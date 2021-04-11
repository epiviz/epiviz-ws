from .Base import Base
from sqlalchemy import Column, Integer, String, ARRAY, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB

class Workspace(Base):
    __tablename__ = 'workspaces'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(), index=True)
    title = Column(String(), nullable=True)
    description = Column(String(), nullable=True)
    genomes = Column(ARRAY(String()), nullable=True)
    tags = Column(ARRAY(String()), nullable=True)
    workspace = Column(JSON, nullable=True)
    workspace_uuid = Column(String(), unique=True, index=True)

    findings = relationship("Finding", back_populates="workspace",
        cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Workspace(name='%s', id='%s')>" % (self.title, self.id)

class Finding(Base):
    __tablename__ = 'findings'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(), nullable=True)

    description = Column(String(), nullable=True)
    gene = Column(String(), nullable=True)
    chrm = Column(String(), nullable=True)
    start = Column(Integer, nullable=True)
    end = Column(Integer, nullable=True)

    genes_in_view = Column(ARRAY(String()), nullable=True)
    chart_markers = Column(JSON, nullable=True)

    user_id = Column(String(), nullable=True)

    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    workspace = relationship("Workspace", back_populates="findings")

    def __repr__(self):
        return "<Finding(id='%s', workspace_id='%s')>" % (self.id, self.workspace_id)