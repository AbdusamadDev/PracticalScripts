from typing import List, Dict, Any
import time
import re
import os

from advanced_index import InvertedIndex as Index
import socket

socket.socket().recv()

class InvertedIndex(object):
    def __init__(self):
        self.__index = dict()

    @staticmethod
    def carve(doc_list: List[str]) -> List:
        # Carve: normalize the given word, remove unnecessary symbols.
        return [re.sub(r'[^\w]', '', word) for word in doc_list]

    def build_index(self, carved_text_list: List, path: Any) -> Any:
        """Builds and appends a normalized and structured value to the main dataset"""
        for index, word in enumerate(carved_text_list):
            prepared_key = self.__index.get(word) or []
            prepared_key.append((path, [index]))
            self.__index[word] = prepared_key

    def add_document(self, path: Any) -> Any:
        try:
            if not os.path.exists(path):
                raise OSError("No such file or directory: {}".format(path))
            if not str(path).endswith(".txt"):
                raise OSError("Path is not a file or not in correct format: {}".format(path))
            # TODO: remove unnecessary chars from read document. Build index
            with open(path, "r") as file:
                normalized_text = file.read().lower().replace("\n", " ").split(" ")
                carved_text_list = self.carve(normalized_text)
                self.build_index(carved_text_list, path)

        except OSError as e:
            raise ValueError("Could not add document: %s" % str(e))

    def search(self, word: str) -> Dict:
        return {word: self.__index.get(word, None)}

    @property
    def display_index(self):
        # Fetch all data and make it read-only
        return self.__index

    @staticmethod
    def populated_add_document(file_path_list):
        for file in file_path_list:
            try:
                doc.add_document(file)
            except Exception:
                continue


if __name__ == '__main__':
    files = ["index.txt", "index2.txt", "inasddex3.txt", "index4.txt", "index5.txt", "index6.txt", "index7.txt",
             "index8.txt", "index9.txt", "index10.txt"]  # Example file paths
    start = time.time()
    doc = InvertedIndex()
    doc.populated_add_document(files)
    print("\n================================")
    print("Target: ", doc.search("purpose"))
    end = time.time()
    print(end - start)
    start = time.time()
    adv = Index()
    adv.process_files(files)

    # print("Inverted Index:", adv.index)
    print("\nSearch results for 'example':", adv.search('purpose'))
    end = time.time()
    print(end - start)
