from typing import Optional


class BaseModelDb:
    id: str
    ts: int
    created: int
    modified: Optional[int]

    def __init__(self, id, ts, created, modified):
        self.id = id
        self.ts = ts
        self.created = created
        self.modified = modified
