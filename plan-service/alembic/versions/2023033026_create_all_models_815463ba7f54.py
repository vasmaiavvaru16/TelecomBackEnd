"""create_all_models

Revision ID: 815463ba7f54
Revises: 
Create Date: 2023-03-30 12:26:29.635834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "815463ba7f54"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plans",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("validity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("plans")
    # ### end Alembic commands ###
