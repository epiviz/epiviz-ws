from sqlalchemy import create_engine  
import os
from uuid import uuid4

DATABASE_URI = os.getenv('DATABASE_URI')

db = create_engine(DATABASE_URI)

with db.connect() as conn:
    conn.execute("ALTER TABLE workspaces DROP COLUMN workspace_uuid;")
    conn.execute("ALTER TABLE workspaces ADD COLUMN workspace_uuid VARCHAR UNIQUE")
    conn.execute("CREATE UNIQUE INDEX uuid_idx ON workspaces (workspace_uuid);")
    rs = conn.execute("select * from workspaces;")

    for r in rs:
        conn.execute("update workspaces set workspace_uuid='" + 
            str(uuid4()).split("-")[0] + "' where id=" + str(r[0]))

    rs = conn.execute("select * from workspaces;")
    for r in rs:
        print(r)


