import string

def generate_keyword_mapping(queries: list) -> dict:
    """
    Creates a mapping of keywords to queries.

    :param queries: a list of queries with responses
    :return: a dictionary of keywords to query indices
    """
    keyword_to_queries = dict()
    for i, question in enumerate(queries):
        if question.get('query'):
            keywords = generate_keywords(question.get("query"))
            keywords.extend(generate_keywords(question.get("response")))
            for keyword in keywords:
                keyword_to_queries.setdefault(keyword, []).append(i)
    return keyword_to_queries


def generate_keywords(query: string) -> list:
    """
    Create a list of keywords from a query.

    :param query: a search query
    :return: the list of keywords from that query
    """
    stop_words = ["", "is", "a", "the", "can",
                  "i", "to", "in", "by", "from", "be", "of",
                  "what", "where", "when", "why", "how", "which"]
    keywords = query \
        .translate(str.maketrans('', '', string.punctuation)) \
        .lower() \
        .split(" ")
    keywords = [word for word in keywords if word not in stop_words]
    return keywords


def search(keyword_to_queries: dict, keywords: list) -> list:
    """
    Looks up the list of queries that satisfy a keyword.

    :param keyword_to_queries: a mapping of keywords to query indices
    :param keywords: a list of keywords to lookup
    :return: a list of query indices
    """
    query_count = dict()
    for keyword in keywords:
        query_indices = keyword_to_queries.get(keyword, [])
        for i in query_indices:
            query_count.setdefault(i, 0)
            query_count[i] += 1
    best_matches = list(
        dict(sorted(query_count.items(), key=lambda item: item[1])).keys())
    return best_matches


def create_md_link(url: string, text: string) -> string:
    """
    Creates a markdown link.

    :param url: the url to link to
    :param text: the text to display
    :return: the markdown link
    """
    if url:
        return f"[{text}]({url})"
    return text
