from models.base_model_db import BaseModelDb


class Well(BaseModelDb):
    name: str
    api: dict
    organizationId: str
    totalStages: int

    def __init__(self, id, ts, created, modified, name, api, organization_id, total_stages):
        super().__init__(id, ts, created, modified)
        self.name = name
        self.api = api
        self.organizationId = organization_id
        self.totalStages = total_stages
