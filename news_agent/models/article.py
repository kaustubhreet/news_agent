from dataclasses import dataclass, field

@dataclass
class Article:
    title: str
    summary: str
    source: str
    link: str = ""
    normalized_title: str = ""
    content_hash: str = ""
