# Security Course Project: SQL Injection and XSS Attacks Demonstration

=
## Description

This project serves as a security course demonstration showcasing how SQL Injection (SQLI) and Cross-Site Scripting (XSS) attacks can be performed on web applications. The website is built using **React** for the frontend and **Flask** for the backend, with a **MySQL** relational database for data storage.

## Features

- **User Registration**: New users can create accounts to access the site.
- **User Login**: Users can log in to their accounts securely.
- **Password Recovery**: Users can recover their forgotten passwords.
- **Password Change**: Users can initiate a password change if they wish.
- **Customer Management**: Users can add and delete their customers.
- **Logout Functionality**: Users can log out of their accounts.

## Technologies Used

- **Frontend**: React
- **Backend**: Flask
- **Database**: MySQL
- **Communication**: Axios for HTTP requests

## Installation

Follow the steps below to set up the project locally.

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your machine.
- **Node.js**: Required for running the React frontend.
- **MySQL**: A MySQL server should be installed and running.
- **Git**: For cloning the repository.

### Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```
### Install Backend Dependencies
```bash
pip install -r requirements.txt
```
### Frontend Setup
1. Navigate to the frontend directory (if applicable):
   ```bash
   cd frontend
   ```
2. Install frontend dependencies using npm:
```bash
npm install
```
### Database Setup
1. Create a new MySQL database for the project.
2. Update the database connection string in your Flask configuration file (e.g., config.py, .env).
3. Ensure the database schema is set up by running any necessary migrations (if applicable).


### Run the Application
1. Start the Flask backend server:
```bash
python main.py
```
2. In a new terminal window, navigate to the frontend directory (if applicable) and start the React application:
```bash
npm start
```
3. Open your browser and go to http://localhost:3000 to access the application.



### Security Vulnerabilities
This project is intended for educational purposes only. The demonstration includes vulnerabilities like SQL Injection and Cross-Site Scripting (XSS) to help users understand and learn about security risks in web applications.


### SQL Injection Example
An example of an SQL injection attack can be demonstrated by modifying the login query with malicious input.

### XSS Example
Cross-site scripting attacks can be illustrated through forms that fail to sanitize user input.




