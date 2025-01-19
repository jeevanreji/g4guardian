# G4Guardian

G4Guardian is a robust web application designed for distributed power grid system monitoring and analytics. Please read the following content to understand how the projct can be set up.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Setup Instructions](#setup-instructions)
   1. [Cloning the Repository](#cloning-the-repository)
   2. [Environment Setup](#environment-setup)
   3. [Database Setup](#database-setup)
   4. [Running the Application](#running-the-application)
4. [Directory Structure](#directory-structure)
5. [Adding Your Own Styles](#adding-your-own-styles)
6. [License](#license)

---

## Features

- User registration and login system with password hashing (using `Werkzeug`).
- Individual dashboards for authenticated users, using unique user IDs.
- Flash messaging for feedback on registration, login, and error states.
- Custom, responsive CSS styling.
- Modular Flask application structure, following blueprints for scalability.

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, Bootstrap, and Font Awesome
- **Database:** SQLite (can be replaced with PostgreSQL, MySQL, etc.)

---

## Setup Instructions

### 1. Cloning the Repository

```bash
# Clone the repository to your local machine
git clone https://github.com/your-username/G4Guardian.git
cd G4Guardian
```

### 2. Environment Setup

1. **Create a Virtual Environment:**

```bash
python -m venv venv
```

2. **Activate the Environment:**

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

### 3. Database Setup

1. **Initialize the Database:**

```bash
flask db init
```

2. **Generate Migration Scripts:**

```bash
flask db migrate -m "Initial migration."
```

3. **Apply Migrations:**

```bash
flask db upgrade
```

4. **Seed the Database (Optional):**
   Add sample data by creating a script in the `scripts` folder or manually via Flask shell:

```bash
flask shell
>>> from app.models import User
>>> from app import db
>>> new_user = User(username="testuser", role="admin", password_hash="hashedpassword")
>>> db.session.add(new_user)
>>> db.session.commit()
>>> exit()
```

### 4. Running the Application

```bash
flask run
```

Navigate to `http://127.0.0.1:5000` to view the application.

---

## Directory Structure

```
G4Guardian/
│
├── app/
│   ├── __init__.py       # Initialize Flask application and database
│   ├── models.py         # Database models (User, etc.)
│   ├── templates/        # HTML files
│   │   ├── index.html    # Home page
│   │   ├── login.html    # Login page
│   │   ├── register.html # Registration page
│   │   └── dashboard.html # User dashboard
│   ├── static/           # Static files (CSS, JS, Images)
│       ├── css/
│       │   └── styles.css
│       └── images/
├── migrations/           # Database migrations folder
├── .env                  # Environment variables
├── config.py             # Configuration settings
├── README.md             # Documentation
├── requirements.txt      # Dependencies
└── run.py                # Application entry point
```

---

## Adding Your Own Styles

To customize the appearance of G4Guardian:

1. Navigate to the `app/static/css` folder.
2. Edit the `styles.css` file or add a new CSS file.
3. Link your new CSS file in the `base.html` template:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/your_new_styles.css') }}">
```

4. Modify styles as needed.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

**Enjoy managing user accounts with G4Guardian!** 🚀

