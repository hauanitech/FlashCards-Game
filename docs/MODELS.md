# API Models

This project uses Pydantic as the BaseModel for our db objects.
Tables are managed through sqlalchemy with the following structure :

Templates for `Table` are already implemented.
make sure to use them in every model you create.

```py
from api.base.models import TableBase

class TableObject(TableBase):
    __tablename__ = "tableobject"
    ...
```

The `TableBase` template already has the default attributes for any object :

```py
class TableBase(Base):
    __abstract__ = True
    id = Column(UUID, primary_key=True, index=True)
    created_at = Column(String)
    updated_at = Column(String)
    created_by = Column(UUID)
```

Imma add further explaination as the project grows.