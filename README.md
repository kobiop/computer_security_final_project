markdown
Copy code
# Security Course Project

This project demonstrates how to perform SQL Injection (SQLI) and Cross-Site Scripting (XSS) attacks on computers. It is built using React for the frontend, Flask for the backend, and MySQL as the relational database.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [Database Configuration](#database-configuration)
- [Usage](#usage)
- [License](#license)

## Project Overview

This web application allows users to:
- Register new accounts.
- Log in to the site.
- Recover their password if forgotten.
- Recover their initiated password if desired.
- Manage their customer list by adding or deleting customers.
- Log out of the application.

## Features
- **User Registration**: Users can create a new account with their details.
- **Login**: Registered users can log into the system.
- **Password Recovery**: Users can recover forgotten passwords.
- **Customer Management**: Users can add or delete customers.
- **Logout**: Users can safely log out of the application.

## Technologies Used
- **Frontend**: React
- **Backend**: Flask
- **Database**: MySQL
- **HTTP Client**: Axios for making API requests between the frontend and backend.

## Frontend Setup

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
Install Frontend Dependencies:

bash
Copy code
npm install
Run the React Application:

bash
Copy code
npm start
The application will be accessible at http://localhost:3000.

Backend Setup
Navigate to the Backend Directory:

bash
Copy code
cd backend
Install Backend Dependencies:

bash
Copy code
pip install -r requirements.txt
Configure the Database:

Create a new database in MySQL (e.g., security_course_db).
Update the database connection string in your configuration file (e.g., config.py) to reflect the newly created database.
Run the Flask Application:

bash
Copy code
python main.py
Once the server is running, you can access the backend API at http://localhost:5000.

Database Configuration
Ensure that MySQL server is running.
Update the connection settings in config.py:
python
Copy code
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/security_course_db'
Usage
After setting up both the frontend and backend, you can register a new user and start exploring the functionalities of the application. Make sure to test for SQL Injection and Cross-Site Scripting vulnerabilities as part of the security course objectives.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
