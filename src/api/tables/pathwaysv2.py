from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, DATE, TSVECTOR

from .database import Base

class Pathways(Base):
    __tablename__ = "pathways"

    catagory = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    pathway = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course_name = Column(VARCHAR(length=255), primary_key=False, nullable=True)
    description = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    compatible_minor = Column(VARCHAR(length=255), primary_key=False, nullable=True)

