import concurrent.futures
import re
import os
from threading import Lock


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.lock = Lock()

    def add_document(self, path):
        """Add a document to the index."""
        if not os.path.exists(path) or not path.endswith(".txt"):
            raise ValueError(f"Invalid file path: {path}")

        with open(path, "r", encoding='utf-8') as file:
            text = file.read().lower()
            words = re.findall(r'\b\w+\b', text)

            with self.lock:
                for position, word in enumerate(words):
                    if word not in self.index:
                        self.index[word] = []
                    self.index[word].append((path, position))

    def search(self, word):
        """Search for a word in the index."""
        return self.index.get(word, [])

    def process_files(self, paths):
        """Process multiple files using concurrent processing."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.add_document, path) for path in paths]
            concurrent.futures.wait(futures)
