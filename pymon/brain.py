import logging
import sqlite3

log = logging.getLogger(__name__)


class Brain: 
    def __init__(self) -> None:
        """
        Initializes the Brain.
        """
        self.connection = self.init_connection("pymon.db")
        self.init_db()
        
    def init_connection(self, name: str):
        """
        Creates a connection to the database by name.
        :param name: the name of the connection
        :return: the database connection
        """
        connection = sqlite3.connect(
            name,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        connection.execute("PRAGMA foreign_keys = 1")
        connection.row_factory = sqlite3.Row
        return connection
        
    def init_db(self):
        """
        Creates the bots database from nothing. 
        
        :return: the database connection
        """

        tables_commands = [
            self.init_queries
        ]

        for command in tables_commands:
            try:
                command()
            except sqlite3.OperationalError:
                log.debug(
                    f"Failure to create table as it already exists: {command}"
                )
                
    def init_queries(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE queries(
            query_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            query VARCHAR, 
            response VARCHAR
        )""")
        
    def init_authors(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE authors(
            author_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            name VARCHAR
        )""")
        