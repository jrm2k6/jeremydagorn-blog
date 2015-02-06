"""create social networks table

Revision ID: 30537f45686e
Revises: None
Create Date: 2015-02-05 22:47:13.264199

"""

# revision identifiers, used by Alembic.
revision = '30537f45686e'
down_revision = None

from alembic import op
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, BOOLEAN, Column


def upgrade():
    op.create_table(
    	'social_network',
    	Column('id', INTEGER, primary_key=True),
    	Column('name', VARCHAR(100), nullable=False),
    	Column('url', NVARCHAR(400), nullable=False),
    	Column('is_shown', BOOLEAN)
    )


def downgrade():
    op.drop('social_network')
