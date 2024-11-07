# Python Authentication System

## Overview
This project demonstrates a backend authentication system in Python with features including password hashing, log filtering, and database authentication using environment variables.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables for database credentials:
   ```bash
   export DB_HOST="your_db_host"
   export DB_NAME="your_db_name"
   export DB_USER="your_db_user"
   export DB_PASSWORD="your_db_password"
   ```

## Features
- Password encryption with bcrypt
- Log filtering for PII
- Authentication via database connection using environment variables

