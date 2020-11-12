from sqlalchemy import create_engine  
import os
from uuid import uuid4

DATABASE_URI = os.getenv('DATABASE_URI')

db = create_engine(DATABASE_URI)

with db.connect() as conn:
    conn.execute("alter table workspaces drop column workspace_uuid;")
    conn.execute("alter table workspaces add column workspace_uuid varchar;")
    rs = conn.execute("select * from workspaces;")

    for r in rs:
        conn.execute("update workspaces set workspace_uuid='" + 
            str(uuid4()).split("-")[0] + "' where id=" + str(r[0]))

    rs = conn.execute("select * from workspaces;")
    for r in rs:
        print(r)


