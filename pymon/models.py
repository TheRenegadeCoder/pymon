from dataclasses import dataclass

@dataclass
class Query:
    query_id: str
    query: str
    response: str
    author: str
    resource: str
