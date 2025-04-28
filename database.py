# database.py
from pymongo import MongoClient

# MongoDB connection URI (replace with your own)
MONGO_URI = "mongodb://your_mongo_connection_string"
client = MongoClient(MONGO_URI)
db = client.get_database("your_database_name")  # Replace with your actual database name
files_collection = db.files  # Assuming you have a collection named 'files'

# Function to search files in MongoDB
def find_files(query):
    # Define a search query (case-insensitive, partial match on file name)
    search_query = {"file_name": {"$regex": query, "$options": "i"}}  # 'i' makes it case-insensitive

    # Search the 'files' collection in MongoDB
    results = list(files_collection.find(search_query))

    # Return the results (list of dictionaries)
    return results
