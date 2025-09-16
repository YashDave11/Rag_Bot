# Cell 4: Load embedding model
from sentence_transformers import SentenceTransformer
from typing import List

print("📥 Loading embedding model...")
# Load the gte-small model using Sentence Transformers
embedding_model = SentenceTransformer("thenlper/gte-small")
print("✅ Embedding model loaded successfully!")

# Define embedding function
def get_embedding(text: str) -> List[float]:
    """
    Generate the embedding for a piece of text.
    
    Args:
        text (str): Text to embed.
    
    Returns:
        List[float]: Embedding of the text as a list.
    """
    embedding = embedding_model.encode(text)
    return embedding.tolist()

# Test the embedding function
test_text = "What are MongoDB best practices?"
test_embedding = get_embedding(test_text)
print(f"✅ Test embedding generated: {len(test_embedding)} dimensions")

print("✅ Cell 4 completed!")
print("Embedding model and function are ready.")