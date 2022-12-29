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
        cur.execute("""CREATE TABLE queries(
            query_id INTEGER PRIMARY KEY,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            query VARCHAR,
            response VARCHAR   
        )""")
        cur.execute("""CREATE VIRTUAL TABLE queries_fts USING FTS5(
            query, 
            response,
            content='queries',
            content_rowid='query_id'
        )""")
        cur.execute("""CREATE TRIGGER query_insert AFTER INSERT ON queries
            BEGIN
                INSERT INTO queries_fts (rowid, query, response)
                VALUES (new.query_id, new.query, new.response);
            END;
        """)
        
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
            url VARCHAR UNIQUE
        )""")
        
    def init_tags(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE tags(
            tag_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            tag VARCHAR UNIQUE
        )""")
        
    def init_author_to_query(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE author_to_query(
            author_to_query_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            author_id INTEGER,
            query_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (author_id),
            FOREIGN KEY (query_id) REFERENCES queries (query_id)
        )""")
        
    def init_resource_to_query(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE resource_to_query(
            resource_to_query_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            resource_id INTEGER,
            query_id INTEGER,
            FOREIGN KEY (resource_id) REFERENCES resources (resource_id),
            FOREIGN KEY (query_id) REFERENCES queries (query_id)
        )""")
        
    def init_tag_to_query(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE tag_to_query(
            tag_to_query_id INTEGER PRIMARY KEY, 
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP, 
            tag_id INTEGER,
            query_id INTEGER,
            FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
            FOREIGN KEY (query_id) REFERENCES queries (query_id),
        )""")
        
    def add_query(self, query: str, response: str, **metadata):
        cur = self.connection.cursor()
        command = "INSERT INTO queries (query, response) VALUES (?, ?)"
        cur.execute(command, (query, response))
        query_id = cur.lastrowid
        if metadata.get("authors"):
            log.debug(f"Adding authors to query: {metadata.get('authors')}")
            for author in metadata.get("authors"):
                command = "INSERT OR IGNORE INTO authors (name) VALUES (?)"
                cur.execute(command, (author, ))
                command = "SELECT * FROM authors WHERE name = ?"
                cur.execute(command, (author, ))
                author_id = cur.fetchone()[0]
                log.debug(f"Added author with ID-{author_id}")
                command = "INSERT INTO author_to_query (author_id, query_id) VALUES (?, ?)"
                cur.execute(command, (author_id, query_id))
        if metadata.get("resources"):
            log.debug(f"Adding resources to query: {metadata.get('resources')}")
            command = "INSERT OR IGNORE INTO resources (url) VALUES (?)"
            cur.executemany(command, [(x, ) for x in metadata.get("resources")])
        if metadata.get("tags"):
            log.debug(f"Adding tags to query: {metadata.get('tags')}")
            command = "INSERT OR IGNORE INTO tags (tag) VALUES (?)"
            cur.executemany(command, [(x, ) for x in metadata.get("tags")])
        self.connection.commit()
        