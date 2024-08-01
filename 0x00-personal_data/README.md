# Personal Data Management and Security

This project focuses on managing and securing personal data by implementing logging, secure database connections, data filtering, and password encryption using Python.

## Project Structure

- **filtered_logger.py**: Contains functions and classes for logging and filtering personal data.
- **encrypt_password.py**: Contains functions for securely hashing and validating passwords.
- **main.py**: Example usage of the functionalities provided by the modules.

## Features

1. **Data Filtering and Logging**:
   - `filter_datum(fields, redaction, message, separator)`: Obfuscates specified fields in a log message using regular expressions.
   - `RedactingFormatter`: Custom logging formatter that uses `filter_datum` to filter out PII fields in log messages.
   - `get_logger()`: Configures and returns a logger that filters out PII data.

2. **Secure Database Connection**:
   - `get_db()`: Establishes a connection to a secure MySQL database using credentials stored in environment variables.

3. **Password Management**:
   - `hash_password(password)`: Hashes a password using bcrypt and returns the salted, hashed password.
   - `is_valid(hashed_password, password)`: Validates a password against a hashed password using bcrypt.

## Environment Variables

To securely connect to the database, the following environment variables need to be set:

- `PERSONAL_DATA_DB_USERNAME`: The database username (default: `"root"`).
- `PERSONAL_DATA_DB_PASSWORD`: The database password (default: `""`).
- `PERSONAL_DATA_DB_HOST`: The database host (default: `"localhost"`).
- `PERSONAL_DATA_DB_NAME`: The name of the database.

## Usage

### Logging and Data Filtering

```python
from filtered_logger import get_logger

logger = get_logger()
logger.info("Sensitive data to be logged...")

