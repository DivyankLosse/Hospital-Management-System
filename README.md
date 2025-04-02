# HappyTots Hospital Management System

A comprehensive hospital management system for managing patients, appointments, and registrations.

## Features

- **User Authentication**: Secure login and signup with email validation and password protection
- **Patient Management**: Add, view, and manage patient information
- **Appointment Scheduling**: Schedule and track patient appointments
- **Dashboard**: Overview of hospital statistics and metrics
- **Modern UI**: Beautiful and intuitive user interface

## Requirements

- Python 3.7+
- PostgreSQL database
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/hospital-management-system.git
   cd hospital-management-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Create a new database for the application
   - Update the database configuration in `.env` file (see `.env.example`)

5. Run the application:
   ```
   python main.py
   ```

## Project Structure

```
├── controller.py             # Database controller with business logic
├── config.py                 # Configuration settings
├── main.py                   # Application entry point
├── gui/                      # GUI components
│   ├── __init__.py
│   ├── splash.py             # Splash screen
│   ├── login/                # Login screen
│   ├── sign_up/              # Sign up screen
│   └── mainwindow/           # Main application window
│       ├── dashboard/        # Dashboard view
│       ├── add_appointment/  # Appointment creation view
│       ├── view_appointment/ # Appointment viewing page
│       ├── inventory/        # Inventory management
│       ├── about/            # About page
│       └── titles/           # Title components
```

## Security Features

- Password hashing using SHA-256
- Input validation for emails and passwords
- Protection against SQL injection through parameterized queries
- Session handling and authentication

## Contributors

- Shruti
- Uttkarsh
- Divyank

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Screenshots

![Login Screen](screenshots/login.png)
![Dashboard](screenshots/dashboard.png)
![Appointments](screenshots/appointments.png)

## Future Enhancements

- Email verification for new accounts
- Role-based access control
- Patient medical records
- Billing and invoicing
- Doctor scheduling
- Pharmacy integration
- Mobile application 