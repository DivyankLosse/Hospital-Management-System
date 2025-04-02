# 🌟 **HappyTots Hospital Management System** 🏥  

A **fun, powerful, and comprehensive** hospital management system designed to streamline patients, appointments, and registrations with a smile! 😊 Built by the dream team: **Divyank**, **Uttkarsh**, and **Shruti**.  

---

## ✨ **What’s HappyTots All About?**  
HappyTots is here to take the stress out of hospital management! From tracking patients to scheduling appointments, we’ve got it all wrapped up in a **modern, intuitive package**—powered by a sprinkle of AI magic and a lot of love. 💙  

---

## 🚀 **Features**  
- 🔒 **User Authentication**: Secure login/signup with email validation and rock-solid password protection.  
- 🧑‍⚕️ **Patient Management**: Add, view, and manage patient info like a pro.  
- 📅 **Appointment Scheduling**: Book and track appointments with ease.  
- 📊 **Dashboard**: Get a bird’s-eye view of hospital stats and metrics.  
- 🎨 **Modern UI**: A beautiful, user-friendly interface that’s a joy to use.  

---

## 🛠️ **Requirements**  
- 🐍 Python 3.7+  
- 🗄️ PostgreSQL database  
- 📦 Required Python packages (check out `requirements.txt`)  

---

## ⚙️ **Installation**  
Ready to get started? Follow these steps:  

1. **Clone the repo**:  
   ```bash
   git clone https://github.com/DivyankLoose/happytots-hospital-system.git
   cd happytots-hospital-system
   ```

2. **Set up a virtual environment**:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**:  
   - Create a shiny new database.  
   - Update the `.env` file with your database details (peek at `.env.example` for guidance).  

5. **Launch the app**:  
   ```bash
   python main.py
   ```

---

## 📂 **Project Structure**  
Here’s how we’ve organized the magic:  
```
├── controller.py             # 🧠 Database logic and brains
├── config.py                 # ⚙️ App settings
├── main.py                   # 🚪 Entry point to the fun
├── gui/                      # 🎨 All the pretty stuff
│   ├── __init__.py
│   ├── splash.py             # 🌈 Splash screen vibes
│   ├── login/                # 🔑 Login goodness
│   ├── sign_up/              # ✍️ Signup flow
│   └── mainwindow/           # 🖼️ Main app hub
│       ├── dashboard/        # 📈 Stats at a glance
│       ├── add_appointment/  # 🕒 Add appointments
│       ├── view_appointment/ # 👀 View appointments
│       ├── inventory/        # 📦 Stock management
│       ├── about/            # ℹ️ About us
│       └── titles/           # 🎀 UI titles
```

---

## 🔐 **Security Features**  
We’ve got your back with:  
- 🔑 Password hashing (SHA-256)  
- ✅ Email and input validation  
- 🛡️ SQL injection protection with parameterized queries  
- 🔒 Secure session handling  

---

## 👩‍💻 **Contributors**  
The brilliant minds behind HappyTots:  
- **Shruti** - UI/UX queen 👑  
- **Uttkarsh** - Code ninja ⚡  
- **Divyank** - AI maestro 🧙‍♂️  

---

## 📜 **License**  
This project is licensed under the **MIT License**—check the `LICENSE` file for details.  

---

## 📸 **Screenshots**  
Peek at the magic in action:  
- ![Login Screen](![image](https://github.com/user-attachments/assets/cb10f251-6cb0-4ad2-ae52-eb3479b10c88))  
- ![Dashboard](![image](https://github.com/user-attachments/assets/b597b647-c06e-434d-873e-a57331b3e2d2))  
- ![Appointments](![image](https://github.com/user-attachments/assets/c75c7c50-ec0e-4bee-be1f-50968bd410dd))  

---

## 🌟 **Future Enhancements**  
We’re dreaming big! Coming soon:  
- 📧 Email verification for new accounts  
- 👥 Role-based access control  
- 🩺 Patient medical records  
- 💸 Billing and invoicing  
- 🩼 Doctor scheduling  
- 💊 Pharmacy integration  
- 📱 Mobile app support  

---
