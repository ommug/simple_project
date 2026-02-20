"""
Chromadb indexer for the data
"""

import chromadb
import numpy as np
import os
from openai import OpenAI
from utils import load_data
from describe_image_openai import DescribeImageOpenAI


class ChromaDBIndexer:
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize the ChromaDB indexer with persistence.
        
        Args:
            persist_directory: Directory path where the index will be saved
        """
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("creators")
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.image_descriptor = DescribeImageOpenAI()

    def embed_description(self, description: str) -> list:
        """
        Embed the description using OpenAI's embedding model
        """
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=description
        )
        return response.data[0].embedding

    def embed_query(self, query: str) -> list:
        """
        Embed the query using OpenAI's embedding model
        """
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        return response.data[0].embedding

    
    def combine_description_embeddings(self, username: str, embeddings: list) -> list:
        """
        Combine multiple embedding vectors for a username using element-wise averaging.
        
        Args:
            username: The username (for reference/logging purposes)
            embeddings: List of embedding vectors (each can be a list or numpy array)
        
        Returns:
            A single embedding vector representing the averaged embeddings
        """
        if not embeddings:
            raise ValueError(f"No embeddings provided for username: {username}")
        
        # Convert all embeddings to numpy arrays for consistent processing
        embeddings_array = np.array(embeddings)
        
        # Compute element-wise average
        averaged_embedding = np.mean(embeddings_array, axis=0)
        
        # Convert back to list for consistency with return type
        return averaged_embedding.tolist()

    def index(self, data: list, num_users: int = 2, num_images_per_user: int = 10):
        """
        Index the data in the collection
        """ 
        user_to_images = {}
        for item in data:
            if "username" in item:
                if item["username"] not in user_to_images:
                    user_to_images[item["username"]] = []
                user_to_images[item["username"]].append(item)
        
        # Process each user's images: get descriptions and create embeddings
        num_users_processed = 0
        for username, images in user_to_images.items():
            if num_users_processed >= num_users:
                break
            num_users_processed += 1
            embeddings = []
            platform = None
            
            for image in images[:num_images_per_user]:
                try:
                    # Get description for the image
                    description = self.image_descriptor.describe_image(image["media_gcs_path"])
                    # Create embedding for the description
                    embedding = self.embed_description(description)
                    embeddings.append(embedding)
                    
                    # Store platform from first image
                    if platform is None:
                        platform = image.get("platform", "unknown")
                except Exception as e:
                    print(f"Error processing image {image.get('media_gcs_path', 'unknown')} for user {username}: {str(e)}")
                    continue
            
            # Combine all embeddings for this user
            if embeddings:
                combined_embedding = self.combine_description_embeddings(username, embeddings)
                print(f"Adding user {username} with platform {platform} and combined {len(embeddings)} embeddings")
                self.collection.add(
                    ids=[username],
                    documents=[username],
                    metadatas=[{"username": username, "platform": platform}],
                    embeddings=[combined_embedding]
                )

    def save_index(self):
        """
        Persist the index to disk. With PersistentClient, data is automatically saved
        on every operation, but this method provides a clear checkpoint.
        """
        # With PersistentClient, data is automatically persisted on every operation
        # This method is here for explicit checkpoint/confirmation
        print(f"Index saved to {self.persist_directory}")

    def search(self, query: str, n_results: int = 10):

        query_embedding = self.embed_query(query)
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results)



if __name__ == "__main__":
    # indexer = ChromaDBIndexer()
    data = load_data("data/records.json")
    # indexer.index(data)
    # indexer.save_index()
    print("Indexed data")