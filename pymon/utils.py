import json
import logging
import os
import string
from urllib.request import urlopen

from dotenv import load_dotenv

log = logging.getLogger(__name__)


def generate_keyword_mapping(queries: list) -> dict:
    """
    Creates a mapping of keywords to queries.

    :param queries: a list of queries with responses
    :return: a dictionary of keywords to query indices
    """
    log.debug(f"Generating keyword mapping from following list: {queries}")
    keyword_to_queries = dict()
    for i, question in enumerate(queries):
        if question.get('query'):
            keywords = generate_keywords(question.get("query"))
            for keyword in keywords:
                keyword_to_queries.setdefault(keyword, {})
                keyword_to_queries[keyword].setdefault(i, 0)
                keyword_to_queries[keyword][i] += 10
            keywords = generate_keywords(question.get("response"))
            for keyword in keywords:
                keyword_to_queries.setdefault(keyword, {})
                keyword_to_queries[keyword].setdefault(i, 0)
                keyword_to_queries[keyword][i] += 1
    log.debug(f"Generated keyword mapping as follows: {keyword_to_queries}")
    return keyword_to_queries


def generate_keywords(query: string) -> list:
    """
    Create a list of keywords from a query.

    :param query: a search query
    :return: the list of keywords from that query
    """
    log.debug(f"Generating keywords from following query: {query}")
    stop_words = ["", "is", "a", "the", "can",
                  "i", "to", "in", "by", "from", "be", "of",
                  "what", "where", "when", "why", "how", "which", "and"]
    keywords = query \
        .translate(str.maketrans('', '', string.punctuation)) \
        .lower() \
        .split(" ")
    keywords = [word for word in keywords if word not in stop_words]
    log.debug(f"Generated list of keywords as follows: {keywords}")
    return keywords


def search(keyword_to_queries: dict, keywords: list) -> list:
    """
    Looks up the list of queries that satisfy a keyword.

    :param keyword_to_queries: a mapping of keywords to query indices
    :param keywords: a list of keywords to lookup
    :return: a list of query indices
    """
    log.debug(
        f"Searching for matching queries from the following list of keywords: {keywords}")
    query_count = dict()
    for keyword in keywords:
        query_indices = keyword_to_queries.get(keyword, {})
        for i, weight in query_indices.items():
            query_count.setdefault(i, 0)
            query_count[i] += weight
    log.debug(f"Generated dictionary of query counts: {query_count}")
    best_matches = list(dict(
        sorted(query_count.items(), key=lambda item: item[1], reverse=True)
    ).keys())
    log.debug(f"Found closest matches as follows: {best_matches}")
    return best_matches


def generate_similar_queries(queries: list, keyword_to_queries: dict) -> None:
    """
    Generates a list of similar queries.

    :param queries: a list of queries
    :param keyword_to_queries: a mapping of keywords to query indices
    """
    log.debug("Adding similar_queries field to queries list")
    for i, query in enumerate(queries):
        if i > 0:
            keywords = generate_keywords(query["query"])
            top_ids = search(keyword_to_queries, keywords)
            top_ids.remove(i)
            query["similar_queries"] = top_ids
            log.debug(f"Updated query to include similar queries: {query}")


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


def load_knowledge() -> tuple[int, list]:
    """
    Loads the bot's knowledge database. Prioritizes the
    KNOWLEDGE_PATH environment variable. KNOWLEDGE_PATH
    can be set to a local file or a remote URL. Otherwise,
    uses the local queries file. 

    :return: a tuple of the type of knowledge database and the
        knowledge database (0 for remote, 1 for local, 2 for default)
    """
    log.debug("Loading Pymon's brain from knowledge path.")
    if path := os.environ.get("KNOWLEDGE_PATH"):
        try:
            data = urlopen(path).read().decode("utf-8")
            return 0, json.loads(data)
        except:
            return 1, json.load(open(path))
    else:
        return 2, json.load(open("queries.json"))


def refresh_knowledge() -> tuple[list, dict]:
    """
    Generates useful information from the knowledge database. 
    Useful when initializing the bot or when the knowledge
    database has been updated.

    :return: a tuple of the knowledge database and a mapping of
        keywords to query indices
    """
    log.debug("Refreshes Pymon's brain assuming new data exists.")
    load_dotenv()
    _, queries = load_knowledge()
    keyword_mapping = generate_keyword_mapping(queries)
    generate_similar_queries(queries, keyword_mapping)
    return queries, keyword_mapping


def generate_tags_set(queries: list) -> set:
    """
    A handy method for processing the set of tags contained in Pymon's
    brain. 

    :param queries: the list of queries from Pymon's brain
    :return: a set of tags represented in Pymon's brain
    """
    log.debug(
        f"Generating the unique set of tags from following list of queries: {queries}")
    tags = set()
    for query in queries:
        query_tags = query.get("tags", [])
        tags |= set(query_tags)
    log.debug(f"Generated list of unique tags as follows: {tags}")
    return tags


def get_queries_from_tag(queries: list, tag: str) -> list[tuple[int, dict]]:
    """
    Given a tag, this function searches Pymon's brain for all the
    matching queries.

    :param queries: Pymon's brain as a list of queries
    :param tag: a tag to lookup
    :return: a list of tuples in the form (query ID, query)
    """
    log.debug(f"Getting set of queries that include the following tag: {tag}")
    matches = list()
    for i, query in enumerate(queries):
        if tag in query.get("tags", []):
            matches.append((i, query))
    log.debug(f"Found queries that match tag as follows: {matches}")
    return matches
