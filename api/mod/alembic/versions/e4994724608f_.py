"""empty message

Revision ID: e4994724608f
Revises: 
Create Date: 2022-04-27 11:51:36.541952

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e4994724608f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("salt", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
