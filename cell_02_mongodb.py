# Cell 2: MongoDB connection (mock for demo)
import os
from pymongo import MongoClient

# Get MongoDB URI from environment
MONGODB_URI = os.environ.get("MONGODB_URI")
print(f"MongoDB URI: {MONGODB_URI}")

# For demo purposes, we'll skip the actual connection
# In real implementation, you would do:
# mongodb_client = MongoClient(MONGODB_URI)
# mongodb_client.admin.command("ping")

print("✅ Cell 2 completed!")
print("📝 Note: Skipping actual MongoDB connection for demo purposes")
print("In real implementation, this would connect to your MongoDB Atlas cluster")