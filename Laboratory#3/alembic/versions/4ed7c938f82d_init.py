"""init

Revision ID: 4ed7c938f82d
Revises: edf136f6eea0
Create Date: 2025-03-10 22:34:55.312504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4ed7c938f82d'
down_revision: Union[str, None] = 'edf136f6eea0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contracts',
    sa.Column('doc_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('file_type', sa.String(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('doc_id')
    )
    op.drop_table('docs')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('docs',
    sa.Column('doc_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('file_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('doc_id', name='docs_pkey')
    )
    op.drop_table('contracts')
    # ### end Alembic commands ###
