"""
Configuration settings for the CS122A Project
"""

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "test",
    "password": "password",
    "database": "cs122a"
}

# File paths
DDL_FILE = "ddl.sql"
NL2SQL_RESULTS_FILE = "nl2sql_results.csv"

# Available commands
COMMANDS = (
    "import",
    "insertAgentClient",
    "addCustomizedModel",
    "deleteBaseModel",
    "listInternetService",
    "countCustomizedModel",
    "topNDurationConfig",
    "listBaseModelKeyWord",
    "printNL2SQLresult"
)

