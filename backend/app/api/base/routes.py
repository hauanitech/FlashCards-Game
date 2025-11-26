import uuid
from datetime import datetime

from core.security import UserDep

def default_post(User: UserDep, Table):
    data = Table(
        id = uuid.uuid4(),
        created_at = datetime.now(),
        updated_at = datetime.now(),
        created_by = uuid.UUID(User["id"])
    )
    return data
