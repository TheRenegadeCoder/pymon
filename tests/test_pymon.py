import json
import os
from urllib.request import urlopen

from dotenv import load_dotenv

import pymon.utils as utils

queries = json.load(open("queries.json"))
keyword_mapping = utils.generate_keyword_mapping(queries)


def top_queries(top_ids):
    return [queries[i]["query"] for i in top_ids]


def test_search_exact_match_first():
    top_ids = utils.search(
        keyword_mapping,
        ["what", "is", "a", "magic", "number"]
    )[:1]
    assert 1 in top_ids
    assert "What is a magic number?" in top_queries(top_ids)


def test_search_exact_match_middle():
    top_ids = utils.search(
        keyword_mapping,
        ["what", "is", "method", "overriding"]
    )[:1]
    assert 13 in top_ids
    assert "What is method overriding?" in top_queries(top_ids)


def test_search_routine_match():
    top_ids = utils.search(
        keyword_mapping,
        ["what", "does", "implements", "mean"]
    )[:3]
    assert 15 in top_ids
    assert "What is the implements relationship?" in top_queries(top_ids)


def test_generate_keyword_mapping():
    test_query = {
        "query": "How now brown cow?",
        "response": "The cow is brown."
    }
    expected_mapping = {
        "brown": {0: 11},  # index: weight
        "cow": {0: 11},
        "now": {0: 10}
    }
    keyword_mapping = utils.generate_keyword_mapping([test_query])
    assert keyword_mapping == expected_mapping


def test_generate_similar_queries():
    utils.generate_similar_queries(queries, keyword_mapping)
    assert 1 not in queries[1]["similar_queries"]


def test_load_knowledge_type_0():
    load_dotenv(dotenv_path=".env.test_type_0")
    actualType, actualKnowledge = utils.load_knowledge()
    expectedType = 0
    data = urlopen("https://raw.githubusercontent.com/TheRenegadeCoder/cs-query-bot/main/queries.json") \
        .read() \
        .decode("utf-8")
    expectedKnowledge = json.loads(data)
    os.environ.pop("KNOWLEDGE_PATH")
    assert expectedType == actualType
    assert expectedKnowledge == actualKnowledge


def test_load_knowledge_type_1():
    load_dotenv(dotenv_path=".env.test_type_1")
    actualType, actualKnowledge = utils.load_knowledge()
    expectedType = 1
    expectedKnowledge = json.load(open("queries.json"))
    os.environ.pop("KNOWLEDGE_PATH")
    assert expectedType == actualType
    assert expectedKnowledge == actualKnowledge


def test_load_knowledge_type_2():
    actualType, actualKnowledge = utils.load_knowledge()
    expectedType = 2
    expectedKnowledge = json.load(open("queries.json"))
    assert expectedType == actualType
    assert expectedKnowledge == actualKnowledge
