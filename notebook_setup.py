import os
# Set up mock environment for demo
os.environ["MONGODB_URI"] = "mongodb+srv://demo:demo@cluster.mongodb.net/demo"
os.environ["SERVERLESS_URL"] = "https://vtqjvgchmwcjwsrela2oyhlegu0hwqnw.lambda-url.us-west-2.on.aws/"

print("✅ Environment variables set up successfully!")
print(f"MONGODB_URI: {os.environ['MONGODB_URI']}")
print(f"SERVERLESS_URL: {os.environ['SERVERLESS_URL']}")