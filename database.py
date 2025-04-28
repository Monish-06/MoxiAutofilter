# database.py
from pymongo import MongoClient

# MongoDB connection URI (replace with your own)
MONGO_URI = "mongodb+srv://monish280720:hsUe1KPZd5wh5hfD@cluster0.x2rr3kl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.get_database("moxi_movies")  # Replace with your actual database name
files_collection = db.Telegram_files  # Assuming you have a collection named 'files'

# Function to search files in MongoDB
def find_files(query):
    # Define a search query (case-insensitive, partial match on file name)
    search_query = {"file_name": {"$regex": query, "$options": "i"}}  # 'i' makes it case-insensitive

    # Search the 'files' collection in MongoDB
    results = list(files_collection.find(search_query))

    # Return the results (list of dictionaries)
    return results
