"""create pivot table for project-technologies relationship

Revision ID: 5aac04af0c32
Revises: 30537f45686e
Create Date: 2015-05-31 20:35:31.676828

"""

# revision identifiers, used by Alembic.
revision = '5aac04af0c32'
down_revision = '30537f45686e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
    	'projects_technologies',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('project_id', sa.Integer, sa.ForeignKey("project.id"), nullable=False),
    	sa.Column('technology_id', sa.Integer, sa.ForeignKey("technology.id"), nullable=False)
    )


def downgrade():
    op.drop_table('projects_technologies')
