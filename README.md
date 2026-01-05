# Database Testing with Python

Demonstrates SQL-driven test validation using pytest and SQLite.

## What This Shows

- Property-based testing for data integrity
- SQL query validation
- Database fixture management
- Test data setup and teardown

## Setup

Create and activate a virtual environment:

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up test database:

**On Mac/Linux:**
```bash
python3 setup_test_db.py
```

**On Windows:**
```bash
python setup_test_db.py
```

## Run Tests

From the project root:
```bash
pytest
```

## Test Coverage

- **Balance Integrity**: Property-based validation that account_balance = deposits - withdrawals
- **User Count**: Validates expected number of test users
- **User Existence**: Checks for specific test users
- **Transaction Status**: Validates transaction completion status
- **User Balance**: Validates individual user balance calculations
- **User Transactions**: Validates transaction history per user