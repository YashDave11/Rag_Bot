# Cell 1: Setup prerequisites
import os
from pymongo import MongoClient
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))
from utils import track_progress

# Set up environment variables
os.environ["MONGODB_URI"] = "mongodb+srv://demo:demo@cluster.mongodb.net/demo"
os.environ["SERVERLESS_URL"] = "https://vtqjvgchmwcjwsrela2oyhlegu0hwqnw.lambda-url.us-west-2.on.aws/"

print("✅ Cell 1 completed successfully!")
print("Environment variables and imports are ready.")