from pymongo import MongoClient

# MongoDB connection URI (replace with your own)
MONGO_URI = "mongodb+srv://monish280720:hsUe1KPZd5wh5hfD@cluster0.x2rr3kl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.get_database("moxi_movies")  # Replace with your actual database name
files_collection = db.Telegram_files  # Assuming you have a collection named 'files'

# Function to search files in MongoDB
def find_files(query, msg=None):
    # Define a search query (case-insensitive, partial match on file name)
    search_query = {"file_name": {"$regex": query, "$options": "i"}}  # 'i' makes it case-insensitive

    try:
        results = list(files_collection.find(search_query))

        # Log the search process
        if not results:
            if msg:
                msg.reply(f"No results found for query: {query}")
            print(f"No results found for query: {query}")
        else:
            if msg:
                msg.reply(f"Found {len(results)} result(s) for query: {query}")
            print(f"Found {len(results)} result(s) for query: {query}")

        return results

    except Exception as e:
        if msg:
            msg.reply(f"Error while searching: {e}")
        print(f"Error while searching: {e}")
        return []
