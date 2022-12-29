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
            self.init_queries,
            self.init_authors,
            self.init_resources,
            self.init_tags,
            self.init_author_to_query,
            self.init_resource_to_query,
            self.init_tag_to_query
        ]

        for command in tables_commands:
            try:
                command()
            except sqlite3.OperationalError:
                log.debug(f"Failure to create table as it already exists: {command}")
                
    def init_queries(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE VIRTUAL TABLE queries USING FTS5(
            query, 
            response
        )""")
        
    def init_authors(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE authors(
            author_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            name VARCHAR UNIQUE
        )""")
        
    def init_resources(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE resources(
            resource_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            url VARCHAR
        )""")
        
    def init_tags(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE tags(
            tag_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            tag VARCHAR
        )""")
        
    def init_author_to_query(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE author_to_query(
            author_to_query_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            author_id INTEGER,
            query_id INTEGER,
            FOREIGN KEY (query_id) REFERENCES queries (rowid),
            FOREIGN KEY (author_id) REFERENCES authors (author_id)
        )""")
        
    def init_resource_to_query(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE resource_to_query(
            resource_to_query_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            resource_id INTEGER,
            query_id INTEGER,
            FOREIGN KEY (query_id) REFERENCES queries (rowid),
            FOREIGN KEY (resource_id) REFERENCES resources (resource_id)
        )""")
        
    def init_tag_to_query(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE tag_to_query(
            tag_to_query_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            tag_id INTEGER,
            query_id INTEGER,
            FOREIGN KEY (query_id) REFERENCES queries (rowid),
            FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
        )""")
        
    def add_query(self, query: str, response: str, **metadata):
        cur = self.connection.cursor()
        command = "INSERT INTO queries (query, response) VALUES (?, ?)"
        cur.execute(command, (query, response))
        query_id = cur.lastrowid
        if metadata.get("authors"):
            log.debug(f"Adding authors to query: {metadata.get('authors')}")
            command = "INSERT OR IGNORE INTO authors (name) VALUES (?)"
            cur.executemany(command, [(x, ) for x in metadata.get("authors")])
            author_id = cur.lastrowid
        self.connection.commit()
        