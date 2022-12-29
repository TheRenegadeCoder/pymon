import logging
import string

from pymon import brain

log = logging.getLogger(__name__)


def create_md_link(url: string, text: string) -> string:
    """
    Creates a markdown link.

    :param url: the url to link to
    :param text: the text to display
    :return: the markdown link
    """
    log.debug(f"Creating markdown link from url ({url}) and text ({text}).")
    if url:
        return f"[{text}]({url})"
    return text


def migrate_v0_to_v1(queries: list, brain: brain.Brain):
    """
    A legacy function for migrating JSON data to a SQLite databse.

    :param queries: a list of queries
    :param brain: the SQLite database connection
    """
    for i, query in enumerate(queries):
        if i != 0:
            log.debug(f"Migrating JSON query to SQLite database: {query}")
            query["authors"] = query.get("credit")
            if query.get("resource"):
                query["resources"] = [query.get("resource")]
            brain.add_query(**query)
