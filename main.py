# coding utf-8
import os
import time
from typing import List
import sqlite3
import multiprocessing
import logging


class SQLExecutor(sqlite3.Connection):
    def __init__(self, db_name, query_strings: List[str]):
        """Force initialization with custom attributes"""
        logging.basicConfig(level=logging.INFO)
        self.db_name = db_name
        self.query = query_strings
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        super().__init__(self.db_name)

    def per_execution(self, query):
        """Execution for each indexes of given array"""
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError:
            logging.info("Skipping due to multiprocessing ")
        except Exception as e:
            logging.warning("Unable to execute query: {}".format(str(e)))

    def parallelized_execution(self):
        """
        Custom execute method with optimal and
        faster boosted with multiprocessing
        """
        for process in self.query:
            p = multiprocessing.Process(target=self.per_execution, args=(process,))
            p.start()
        self.connection.close()


if __name__ == '__main__':
    queries = [
        """CREATE TABLE IF NOT EXISTS test (name TEXT);""",
        """INSERT INTO test (name) VALUES ('Testing')""",
        """INSERT INTO test (name) VALUES ('asdasdasd')"""
    ]
    start = time.time()
    executor = SQLExecutor("testing.db", query_strings=queries)
    executor.parallelized_execution()
    end = time.time()
    print(end - start)
    new_start = time.time()
    another_task = sqlite3.connect("new.db")
    cursor = another_task.cursor()
    for i in queries:
        cursor.execute(i)
    another_task.commit()
    another_task.close()
    new_end = time.time()
    print(new_end - new_start)
    os.remove("new.db")
    os.remove("testing.db")
