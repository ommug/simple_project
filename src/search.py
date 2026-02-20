"""

Search the data using the chromadb indexer
"""

from indexer import ChromaDBIndexer
import argparse

class Search:
    def __init__(self):
        self.indexer = ChromaDBIndexer()

    def search(self, query: str, n_results: int = 10):
        return self.indexer.search(query, n_results)


if __name__ == "__main__":
    search = Search()

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--n_results", type=int, required=False, default=1)
    args = parser.parse_args()  
    
    results = search.search(args.query, args.n_results)
    
    # ChromaDB query returns a dict with 'ids', 'documents', 'metadatas', 'distances'
    if results and "ids" in results and len(results["ids"]) > 0:
        for i in range(len(results["ids"][0])):
            print(f"\nResult {i+1}:")
            print(f"  ID: {results['ids'][0][i]}")
            print(f"  Document: {results['documents'][0][i]}")
            print(f"  Metadata: {results['metadatas'][0][i]}")
            if "distances" in results and results["distances"]:
                print(f"  Distance: {results['distances'][0][i]:.4f}")
    else:
        print("No results found.")