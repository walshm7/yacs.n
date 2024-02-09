"""CoursesMaster table

Revision ID: ffaaeebb8125
Revises: c959c263997f
Create Date: 2023-04-06 00:55:10.389370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffaaeebb8125'  # randomly created an 'unique id' with 12 hex characters
down_revision = 'c959c263997f'  # grab value from previous version file
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pathways',
    sa.Column('catagory', sa.VARCHAR(length=255), nullable=False),
    sa.Column('pathway', sa.VARCHAR(length=255), nullable=False),
    sa.Column('course', sa.VARCHAR(length=255), nullable=False),
    sa.Column('course_name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), nullable=False),
    sa.Column('compatible_minor', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('catagory', 'pathway', 'course', 'course_name', 'description')
    )
    '''catagory = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    pathway = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    description = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    compatible_minor = Column(VARCHAR(length=255), primary_key=True, nullable=False)'''
