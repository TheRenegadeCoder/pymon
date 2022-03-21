import json
from code_bot_utils import *

queries = json.load(open("queries.json"))
keyword_mapping = generate_keyword_mapping(queries)

def top_queries(top_ids):
    return [queries[i]["query"] for i in top_ids]

def test_search_exact_match_first():
    top_ids = search(keyword_mapping, ["what", "is", "a", "magic", "number"])[:1]
    assert 1 in top_ids
    assert "What is a magic number?" in top_queries(top_ids)

def test_search_exact_match_middle():
    top_ids = search(keyword_mapping, ["what", "is", "method", "overriding"])[:1]
    assert 12 in top_ids
    assert "What is method overriding?" in top_queries(top_ids)

def test_search_routine_match():
    top_ids = search(keyword_mapping, ["what", "does", "implements", "mean"])[:3]
    assert 14 in top_ids
    assert "What is the implements relationship?" in top_queries(top_ids)

def test_generate_keyword_mapping():
    test_query = {
        "query": "How now brown cow?",
        "response": "The cow is brown."
    }
    expected_mapping = {
        "brown": {0: 11},
        "cow": {0: 11},
        "now": {0: 10}
    }
    keyword_mapping = generate_keyword_mapping([test_query])
    assert keyword_mapping == expected_mapping
