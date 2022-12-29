from dataclasses import dataclass, field


@dataclass
class Query:
    query_id: str
    query: str
    response: str
    authors: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
