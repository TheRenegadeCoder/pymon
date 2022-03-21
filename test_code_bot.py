import json
from code_bot_utils import *

queries = json.load(open("queries.json"))
keyword_mapping = generate_keyword_mapping(queries)

def top_queries(top_ids):
    return [queries[i]["query"] for i in top_ids]

def test_search_exact_match_first():
    top_ids = search(keyword_mapping, ["what", "is", "a", "magic", "number"])[:3]
    assert 1 in top_ids
    assert "What is a magic number?" in top_queries(top_ids)

def test_search_exact_match_middle():
    top_ids = search(keyword_mapping, ["what", "is", "method", "overriding"])[:3]
    assert 12 in top_ids
    assert "What is method overriding?" in top_queries(top_ids)
