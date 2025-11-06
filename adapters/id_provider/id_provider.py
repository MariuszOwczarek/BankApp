import uuid
from domain.ports.ports import IdProvider

class UUIDIdProvider(IdProvider):
    name = "uuid4"

    def generate_id(self) -> str:
        return str(uuid.uuid4())