from datetime import datetime

from . import BaseModel
from . import Status


class Chat(BaseModel):
    chat_id: int
    name: str
    topic: str
    read_privileges: int
    write_privileges: int
    auto_join: bool
    instance: bool

    status: Status
    updated_at: datetime
    created_at: datetime
    created_by: int
