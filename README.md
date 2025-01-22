MongoDB Query Handler

This repository provides a streamlined and flexible way to query MongoDB collections using Python. The provided code supports complex filter conditions, projection of specific fields, and seamless integration with Pandas for data analysis.
Features

    Dynamic MongoDB Connection: Connect to any MongoDB database by providing a configuration file.
    Flexible Querying: Supports logical operations for building complex filters.
    ObjectId Handling: Automatically manages ObjectId conversion for seamless querying.
    DataFrame Integration: Converts MongoDB query results into Pandas DataFrame for further processing.

Installation

Ensure the following are installed:

    Python 3.x
    Required Python packages: mongoengine, pandas, bson

Install dependencies using pip:

pip install mongoengine pandas

Usage
Configuration

Create a configuration file db_config.json with the following structure:

{
  "mongo_url": "your_mongo_url",
  "db_name": "your_database_name"
}

Example Code

from datetime import datetime
from mongoengine.queryset.visitor import Q
from your_module_name import get_mongo_data

# Example query
recent_transactions = get_mongo_data(
    collection_name='transactions',
    filter_conditions=(
        Q(updated_at__gte=datetime(2024, 1, 1)) &
        Q(status='SUCCESS') &
        Q(amount__gte=1000)
    ),
    columns_needed=['_id', 'user_id', 'amount', 'status', 'updated_at']
)

# Display results
print(recent_transactions.head())

Explanation

    Filter Conditions: Use Q objects for complex queries with logical operators (& for AND, | for OR).
    Columns Needed: Specify which fields to include in the output.

Notes

    Replace placeholders in the configuration file with actual connection details.
    Modify filter conditions and columns based on your specific use case.

License

This project is open source under the MIT license. Contributions are welcome!