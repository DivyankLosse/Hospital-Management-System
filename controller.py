import psycopg2
import os
from config import config
from dotenv import load_dotenv
import hashlib
import logging
import re
from contextlib import contextmanager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='hospital_system.log'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Database connection parameters
DB_PARAMS = {
    "host": config.get("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": config.get("DB_NAME"),
    "port": "5432",
}

# Context manager for database connections
@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = psycopg2.connect(**DB_PARAMS)
        yield connection
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if connection:
            connection.close()

# Context manager for cursor
@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        try:
            yield cursor
            if commit:
                connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            cursor.close()

# Hash password for security
def hash_password(password):
    # Use SHA-256 for password hashing (in production, use more secure methods like bcrypt)
    return hashlib.sha256(password.encode()).hexdigest()

# Create tables if they don't exist
def initialize_tables():
    try:
        with get_db_cursor(commit=True) as cursor:
            # Users table for login/signup with hashed passwords
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Patient appointments table (unchanged)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patient_appointments (
                    appointment_id SERIAL PRIMARY KEY,
                    patient_name VARCHAR(100) NOT NULL,
                    phone_no VARCHAR(15) NOT NULL,
                    address TEXT,
                    gender VARCHAR(10),
                    age INT,
                    appointment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'Pending'
                )
            """)
            
            # Inventory table for tracking hospital inventory
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    item_id SERIAL PRIMARY KEY,
                    category VARCHAR(50) NOT NULL,
                    item_name VARCHAR(100) NOT NULL,
                    quantity INT NOT NULL,
                    unit_price DECIMAL(10, 2),
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing tables: {e}")
        raise

# User Management Functions
def signup_new_user(username, password):
    # Validate email format
    if not is_valid_email(username):
        return False
        
    # Validate password strength
    if len(password) < 6:
        return False
    
    try:
        hashed_password = hash_password(password)
        with get_db_cursor(commit=True) as cursor:
            cmd = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(cmd, (username, hashed_password))
        logger.info(f"New user created: {username}")
        return True
    except psycopg2.IntegrityError:
        logger.warning(f"Username already exists: {username}")
        return False  # Username already exists
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise

def check_user(username, password):
    try:
        hashed_password = hash_password(password)
        with get_db_cursor() as cursor:
            cmd = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
            cursor.execute(cmd, (username, hashed_password))
            result = cursor.fetchone()[0] >= 1
            if result:
                logger.info(f"User login successful: {username}")
            else:
                logger.warning(f"Failed login attempt for user: {username}")
            return result
    except Exception as e:
        logger.error(f"Error checking user credentials: {e}")
        raise

def update_username(old_username, password, new_username):
    try:
        hashed_password = hash_password(password)
        with get_db_cursor(commit=True) as cursor:
            cmd = "UPDATE users SET username=%s WHERE username=%s AND password=%s"
            cursor.execute(cmd, (new_username, old_username, hashed_password))
            
            cmd = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
            cursor.execute(cmd, (new_username, hashed_password))
            result = cursor.fetchone()[0] >= 1
            if result:
                logger.info(f"Username updated: {old_username} -> {new_username}")
            return result
    except psycopg2.IntegrityError:
        logger.warning(f"Update failed - new username already exists: {new_username}")
        return False
    except Exception as e:
        logger.error(f"Error updating username: {e}")
        raise

# Patient Appointment Functions
def add_patient_appointment(patient_name, phone_no, address, gender, age):
    try:
        with get_db_cursor(commit=True) as cursor:
            cmd = """INSERT INTO patient_appointments 
                    (patient_name, phone_no, address, gender, age) 
                    VALUES (%s, %s, %s, %s, %s) 
                    RETURNING appointment_id"""
            cursor.execute(cmd, (patient_name, phone_no, address, gender, age))
            appointment_id = cursor.fetchone()[0]
            logger.info(f"New appointment added for patient: {patient_name}, ID: {appointment_id}")
            return appointment_id
    except Exception as e:
        logger.error(f"Error adding patient appointment: {e}")
        raise

def get_all_appointments():
    try:
        with get_db_cursor() as cursor:
            cmd = """SELECT appointment_id, patient_name, phone_no, address, gender, age, 
                    appointment_date, status 
                    FROM patient_appointments 
                    ORDER BY appointment_date DESC"""
            cursor.execute(cmd)
            result = cursor.fetchall()
            logger.info(f"Retrieved {len(result)} appointments")
            return result
    except Exception as e:
        logger.error(f"Error retrieving appointments: {e}")
        raise

def update_appointment_status(appointment_id, new_status):
    try:
        with get_db_cursor(commit=True) as cursor:
            cmd = "UPDATE patient_appointments SET status=%s WHERE appointment_id=%s"
            cursor.execute(cmd, (new_status, appointment_id))
            logger.info(f"Updated appointment ID {appointment_id} status to: {new_status}")
            return True
    except Exception as e:
        logger.error(f"Error updating appointment status: {e}")
        raise
        
def delete_appointment(appointment_id):
    """Delete an appointment from the database"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cmd = "DELETE FROM patient_appointments WHERE appointment_id=%s"
            cursor.execute(cmd, (appointment_id,))
            logger.info(f"Deleted appointment ID: {appointment_id}")
            return True
    except Exception as e:
        logger.error(f"Error deleting appointment: {e}")
        raise

def get_appointment_details(appointment_id):
    try:
        with get_db_cursor() as cursor:
            cmd = """SELECT appointment_id, patient_name, phone_no, address, gender, age, 
                    appointment_date, status 
                    FROM patient_appointments 
                    WHERE appointment_id=%s"""
            cursor.execute(cmd, (appointment_id,))
            result = cursor.fetchone()
            if result:
                logger.info(f"Retrieved details for appointment ID: {appointment_id}")
            else:
                logger.warning(f"No appointment found with ID: {appointment_id}")
            return result
    except Exception as e:
        logger.error(f"Error retrieving appointment details: {e}")
        raise

# Inventory Management Functions
def add_inventory_item(category, item_name, quantity, unit_price=0.0):
    """Add a new item to inventory or update quantity if already exists"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # Check if item already exists
            cursor.execute("SELECT item_id, quantity FROM inventory WHERE category=%s AND item_name=%s", 
                         (category, item_name))
            existing_item = cursor.fetchone()
            
            if existing_item:
                # Update existing item
                item_id, current_quantity = existing_item
                new_quantity = current_quantity + quantity
                cursor.execute("UPDATE inventory SET quantity=%s, unit_price=%s, last_updated=CURRENT_TIMESTAMP WHERE item_id=%s",
                            (new_quantity, unit_price, item_id))
                logger.info(f"Updated inventory item: {item_name}, new quantity: {new_quantity}")
                return item_id
            else:
                # Insert new item
                cursor.execute("""INSERT INTO inventory 
                               (category, item_name, quantity, unit_price) 
                               VALUES (%s, %s, %s, %s) 
                               RETURNING item_id""", 
                              (category, item_name, quantity, unit_price))
                item_id = cursor.fetchone()[0]
                logger.info(f"Added new inventory item: {item_name}, quantity: {quantity}")
                return item_id
    except Exception as e:
        logger.error(f"Error adding inventory item: {e}")
        raise
        
def get_inventory_items(category=None):
    """Get all inventory items, optionally filtered by category"""
    try:
        with get_db_cursor() as cursor:
            if category:
                cursor.execute("""SELECT item_id, category, item_name, quantity, unit_price, last_updated 
                               FROM inventory 
                               WHERE category=%s 
                               ORDER BY category, item_name""", (category,))
            else:
                cursor.execute("""SELECT item_id, category, item_name, quantity, unit_price, last_updated 
                               FROM inventory 
                               ORDER BY category, item_name""")
            
            result = cursor.fetchall()
            logger.info(f"Retrieved {len(result)} inventory items")
            return result
    except Exception as e:
        logger.error(f"Error retrieving inventory items: {e}")
        raise

def update_inventory_quantity(item_id, new_quantity):
    """Update the quantity of an inventory item"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("UPDATE inventory SET quantity=%s, last_updated=CURRENT_TIMESTAMP WHERE item_id=%s",
                         (new_quantity, item_id))
            logger.info(f"Updated inventory item ID {item_id} quantity to: {new_quantity}")
            return True
    except Exception as e:
        logger.error(f"Error updating inventory quantity: {e}")
        raise

def delete_inventory_item(item_id):
    """Delete an inventory item"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM inventory WHERE item_id=%s", (item_id,))
            logger.info(f"Deleted inventory item ID: {item_id}")
            return True
    except Exception as e:
        logger.error(f"Error deleting inventory item: {e}")
        raise
        
def get_inventory_categories():
    """Get all unique inventory categories"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT DISTINCT category FROM inventory ORDER BY category")
            result = [row[0] for row in cursor.fetchall()]
            return result
    except Exception as e:
        logger.error(f"Error retrieving inventory categories: {e}")
        raise

# Utility Functions
def human_format(num):
    if num < 1000:
        return num
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    return "%.1f%s" % (num, ["", "K", "M", "G", "T", "P"][magnitude])

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Get appointment statistics
def get_appointment_stats():
    try:
        with get_db_cursor() as cursor:
            # Get total appointments
            cursor.execute("SELECT COUNT(*) FROM patient_appointments")
            total = cursor.fetchone()[0]
            
            # Get pending appointments
            cursor.execute("SELECT COUNT(*) FROM patient_appointments WHERE status='Pending'")
            pending = cursor.fetchone()[0]
            
            # Get completed appointments
            cursor.execute("SELECT COUNT(*) FROM patient_appointments WHERE status='Completed'")
            completed = cursor.fetchone()[0]
            
            # Get cancelled appointments
            cursor.execute("SELECT COUNT(*) FROM patient_appointments WHERE status='Cancelled'")
            cancelled = cursor.fetchone()[0]
            
            return {
                "total": total,
                "pending": pending,
                "completed": completed,
                "cancelled": cancelled
            }
    except Exception as e:
        logger.error(f"Error getting appointment statistics: {e}")
        raise

# Initialize tables when the controller is imported
try:
    initialize_tables()
except Exception as e:
    logger.critical(f"Failed to initialize database tables: {e}")
    print(f"Database initialization error: {e}")