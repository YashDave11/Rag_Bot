# Cell 3: Load data into MongoDB (mock version)
import json
from pathlib import Path

# Database and collection names
DB_NAME = "mongodb_genai_devday_agents"
FULL_COLLECTION_NAME = "mongodb_docs"
VS_COLLECTION_NAME = "mongodb_docs_embeddings"
VS_INDEX_NAME = "vector_index"

print(f"Database: {DB_NAME}")
print(f"Vector Search Collection: {VS_COLLECTION_NAME}")
print(f"Full Documents Collection: {FULL_COLLECTION_NAME}")
print(f"Vector Index: {VS_INDEX_NAME}")

# Load and show data structure
data_dir = Path(__file__).parent / "data"

# Load vector search data
with open(data_dir / f"{VS_COLLECTION_NAME}.json", "r") as f:
    vs_data = json.load(f)

# Load full documents
with open(data_dir / f"{FULL_COLLECTION_NAME}.json", "r") as f:
    full_data = json.load(f)

print(f"✅ Loaded {len(vs_data)} documents with embeddings")
print(f"✅ Loaded {len(full_data)} full documents")

# Show sample structure
if vs_data:
    sample = vs_data[0]
    print(f"📊 Sample document keys: {list(sample.keys())}")
    print(f"📊 Embedding dimensions: {len(sample.get('embedding', []))}")

print("✅ Cell 3 completed!")
print("📝 Data loaded successfully (mock version)")