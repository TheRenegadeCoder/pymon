import logging
import sqlite3
from collections import defaultdict

from pymon import models

log = logging.getLogger(__name__)


class Brain:
    def __init__(self) -> None:
        """
        Initializes the Brain.
        """
        self.connection = self.init_connection("pymon.db")
        self.init_db()
        queries = self.search("recursion")
        log.debug(f"TEST: {queries}")

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
            self.init_tag_to_query,
            self.init_triggers
        ]

        for command in tables_commands:
            try:
                command()
            except sqlite3.OperationalError:
                log.warning(f"Failure to run database command: {command}")

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
            FOREIGN KEY (query_id) REFERENCES queries (query_id)
        )""")

    def init_triggers(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TRIGGER query_insert AFTER INSERT ON queries
            BEGIN
                INSERT INTO queries_fts (rowid, query, response)
                VALUES (new.query_id, new.query, new.response);
            END;
        """)

    def add_query(self, query: str, response: str, **metadata) -> int:
        """
        A handy method for adding queries into the database.

        :param query: the question to ask
        :param response: the answer to that question
        """
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
                command = "INSERT INTO author_to_query (author_id, query_id) VALUES (?, ?)"
                cur.execute(command, (author_id, query_id))
        if metadata.get("resources"):
            log.debug(
                f"Adding resources to query: {metadata.get('resources')}")
            for resource in metadata.get('resources'):
                command = "INSERT OR IGNORE INTO resources (url) VALUES (?)"
                cur.execute(command, (resource, ))
                command = "SELECT * FROM resources WHERE url = ?"
                cur.execute(command, (resource, ))
                resource_id = cur.fetchone()[0]
                command = "INSERT INTO resource_to_query (resource_id, query_id) VALUES (?, ?)"
                cur.execute(command, (resource_id, query_id))
        if metadata.get("tags"):
            log.debug(f"Adding tags to query: {metadata.get('tags')}")
            for tag in metadata.get("tags"):
                command = "INSERT OR IGNORE INTO tags (tag) VALUES (?)"
                cur.execute(command, (tag, ))
                command = "SELECT * FROM tags WHERE tag = ?"
                cur.execute(command, (tag, ))
                tag_id = cur.fetchone()[0]
                command = "INSERT INTO tag_to_query (tag_id, query_id) VALUES (?, ?)"
                cur.execute(command, (tag_id, query_id))
        self.connection.commit()
        return query_id

    def get_query(self, index: int) -> models.Query:
        """
        Retrieves a query by its index.
        
        :param index: the index of the query as an integer
        """
        cur = self.connection.cursor()
        command = """
            SELECT 
                queries.query_id,
                query, 
                response,
                authors.name,
                resources.url,
                tags.tag
            FROM 
                queries
            LEFT JOIN author_to_query
                ON author_to_query.query_id = queries.query_id
            LEFT JOIN authors
                ON author_to_query.author_id = authors.author_id
            LEFT JOIN resource_to_query
                ON resource_to_query.query_id = queries.query_id
            LEFT JOIN resources
                ON resource_to_query.resource_id = resources.resource_id
            LEFT JOIN tag_to_query
                ON tag_to_query.query_id = queries.query_id
            LEFT JOIN tags
                ON tag_to_query.tag_id = tags.tag_id
            WHERE 
                queries.query_id = ?
        """
        matches = cur.execute(command, (index, )).fetchall()
        log.debug(f"Retrieved query: {matches}")

        row = list(zip(*matches))
        log.debug(row)

        return models.Query(
            query_id=list(set(row[0]))[0],
            query=list(set(row[1]))[0],
            response=list(set(row[2]))[0],
            authors=list(set(row[3])) if row[3][0] else [],
            resources=list(set(row[4])) if row[4][0] else [],
            tags=list(set(row[5])) if row[5][0] else []
        )

    def get_tags(self) -> list[str]:
        """
        Retrieves the unique list of tags in alphabetical order.
        """
        cur = self.connection.cursor()
        command = """
            SELECT
                tag
            FROM
                tags
            ORDER BY
                tag
        """
        tags = cur.execute(command).fetchall()
        return [tag[0] for tag in tags]

    def get_queries_by_tag(self, tag: str) -> list[models.Query]:
        """
        Retrieves all queries matching the given tag.

        :param tag: the tag to lookup
        """
        cur = self.connection.cursor()
        command = """
            SELECT
                queries.query_id,
                query, 
                response,
                authors.name,
                resources.url,
                tags.tag
            FROM
                queries
            LEFT JOIN author_to_query
                ON author_to_query.query_id = queries.query_id
            LEFT JOIN authors
                ON author_to_query.author_id = authors.author_id
            LEFT JOIN resource_to_query
                ON resource_to_query.query_id = queries.query_id
            LEFT JOIN resources
                ON resource_to_query.resource_id = resources.resource_id
            LEFT JOIN tag_to_query
                ON tag_to_query.query_id = queries.query_id
            LEFT JOIN tags
                ON tag_to_query.tag_id = tags.tag_id
            WHERE
                tags.tag = ?
        """
        matches = cur.execute(command, (tag, )).fetchall()
        log.debug(f"Retrieved queries by tag ({tag}): {matches}")

        groups = defaultdict(list)
        for match in matches:
            groups[match["query_id"]].append(match)

        results = []
        for group in groups.values():
            row = list(zip(*group))
            results.append(models.Query(
                query_id=list(set(row[0]))[0],
                query=list(set(row[1]))[0],
                response=list(set(row[2]))[0],
                authors=list(set(row[3])) if row[3][0] else [],
                resources=list(set(row[4])) if row[4][0] else [],
                tags=list(set(row[5])) if row[5][0] else []
            ))

        return results

    def search(self, key_phrase: str) -> list[models.Query]:
        """
        Searches the queries table for matching searches.

        :param key_phrase: the phrase to search up
        :return: a list of queries that match the user's search phrase
        """
        cur = self.connection.cursor()
        command = """
            SELECT 
                queries_fts.rowid,
                query, 
                response,
                authors.name,
                resources.url,
                tags.tag
            FROM 
                queries_fts 
            LEFT JOIN author_to_query
                ON author_to_query.query_id = queries_fts.rowid
            LEFT JOIN authors
                ON author_to_query.author_id = authors.author_id
            LEFT JOIN resource_to_query
                ON resource_to_query.query_id = queries_fts.rowid
            LEFT JOIN resources
                ON resource_to_query.resource_id = resources.resource_id
            LEFT JOIN tag_to_query
                ON tag_to_query.query_id = queries_fts.rowid
            LEFT JOIN tags
                ON tag_to_query.tag_id = tags.tag_id
            WHERE 
                queries_fts MATCH ? 
            ORDER BY 
                rank
        """
        matches = cur.execute(command, (key_phrase, )).fetchall()
        log.debug(f"Retrieved search results: {matches}")

        groups = defaultdict(list)
        for match in matches:
            groups[match["rowid"]].append(match)

        results = []
        for group in groups.values():
            row = list(zip(*group))
            results.append(models.Query(
                query_id=list(set(row[0]))[0],
                query=list(set(row[1]))[0],
                response=list(set(row[2]))[0],
                authors=list(set(row[3])) if row[3][0] else [],
                resources=list(set(row[4])) if row[4][0] else [],
                tags=list(set(row[5])) if row[5][0] else []
            ))

        return results
    
    def get_all_queries(self) -> list[models.Query]:
        """
        A handy method for pulling out all of the queries in the database.
        """
        cur = self.connection.cursor()
        command = """
            SELECT
                queries.query_id,
                query, 
                response,
                authors.name,
                resources.url,
                tags.tag
            FROM
                queries
            LEFT JOIN author_to_query
                ON author_to_query.query_id = queries.query_id
            LEFT JOIN authors
                ON author_to_query.author_id = authors.author_id
            LEFT JOIN resource_to_query
                ON resource_to_query.query_id = queries.query_id
            LEFT JOIN resources
                ON resource_to_query.resource_id = resources.resource_id
            LEFT JOIN tag_to_query
                ON tag_to_query.query_id = queries.query_id
            LEFT JOIN tags
                ON tag_to_query.tag_id = tags.tag_id
        """
        matches = cur.execute(command).fetchall()

        groups = defaultdict(list)
        for match in matches:
            groups[match["query_id"]].append(match)

        results = []
        for group in groups.values():
            row = list(zip(*group))
            results.append(models.Query(
                query_id=list(set(row[0]))[0],
                query=list(set(row[1]))[0],
                response=list(set(row[2]))[0],
                authors=list(set(row[3])) if row[3][0] else [],
                resources=list(set(row[4])) if row[4][0] else [],
                tags=list(set(row[5])) if row[5][0] else []
            ))

        return results
