import pandas as pd
import chromadb
import uuid
from pathlib import Path


class Portfolio:
    def __init__(self, file_path=None):
        if file_path is None:
            # Get the directory where this file (portfolio.py) is located
            current_dir = Path(__file__).parent
            file_path = current_dir / "resource" / "my_portfolio.csv"
        else:
            file_path = Path(file_path)

        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])