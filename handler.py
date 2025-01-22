from mongoengine import connect, DynamicDocument
import pandas as pd
import json
from datetime import datetime
from bson import ObjectId
from mongoengine.queryset.visitor import Q

class MongoDocument(DynamicDocument):
    meta = {'abstract': True, 'strict': False}

def connect_to_db(config_path):
    """Connect to MongoDB using configuration details."""
    with open(config_path, 'r') as fp:
        config = json.load(fp)
    
    mongo_host = config.get('mongo_url')
    db_name = config.get('db_name', 'defaultDB')
    connect(db_name, host=mongo_host)

def get_objectid_fields(collection_name):
    """Retrieve a sample document to determine ObjectId fields."""
    class DynamicCollection(MongoDocument):
        meta = {'collection': collection_name}
    
    sample_doc = DynamicCollection.objects.first()
    if sample_doc:
        return [field for field, value in sample_doc.to_mongo().items() if isinstance(value, ObjectId)]
    return []

def convert_filter_conditions(filter_conditions, collection_name):
    """Convert string representations of ObjectId to ObjectId for any ObjectId fields."""
    objectid_fields = get_objectid_fields(collection_name)
    
    if filter_conditions is not None:
        for key, value in filter_conditions.items():
            if key in objectid_fields and isinstance(value, str):
                filter_conditions[key] = ObjectId(value)  # Convert string to ObjectId
    return filter_conditions

def convert_objectid_to_string(data):
    """Convert ObjectId fields in the document to strings."""
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)  # Convert ObjectId to string
    return data

def documents_to_dataframe(documents):
    """Convert documents to pandas DataFrame, handling ObjectId conversion."""
    return pd.DataFrame([convert_objectid_to_string(doc.to_mongo().to_dict()) for doc in documents])

def query_collection(config_path, collection_name, filter_conditions=None, columns_needed=None):
    """Query a MongoDB collection and return matching documents."""
    connect_to_db(config_path)
    
    class DynamicCollection(MongoDocument):
        meta = {'collection': collection_name}

    query = DynamicCollection.objects()
    
    if filter_conditions:
        query = query.filter(filter_conditions)  # Accepts Q objects for complex queries
    
    if columns_needed:
        query = query.only(*columns_needed)
    
    return list(query)

def get_mongo_data(config_path, collection_name, filter_conditions=None, columns_needed=None):
    """Fetch and convert MongoDB data into a DataFrame."""
    documents = query_collection(config_path, collection_name, filter_conditions, columns_needed)
    df = documents_to_dataframe(documents)
    return df
