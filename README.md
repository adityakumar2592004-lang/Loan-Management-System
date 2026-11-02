# AIWIZE Loan Management System

A full-stack Loan Management System built using Python Flask, PostgreSQL, HTML, CSS, and JavaScript.

## Features
- Customer registration and loan application
- PostgreSQL database integration
- Dashboard with loan statistics
- Recent loan applications table
- Customer records table
- EMI calculator
- Automatic dashboard data refresh

## Tech Stack
- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Database Tool:** pgAdmin 4

## Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/adityakumar2592004-lang/Loan-Management-System.git
   ```

2. Open the project folder:
   ```bash
   cd Loan-Management-System
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file and add your PostgreSQL password:
   ```env
   DATABASE_PASSWORD=your_postgresql_password
   ```

6. Create the PostgreSQL database named `Financial_DB` and configure the required tables.

7. Run the application:
   ```bash
   python app.py
   ```

8. Open `http://127.0.0.1:5000/` in your browser.

## Note
This project is developed for learning and demonstration purposes.