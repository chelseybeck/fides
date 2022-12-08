"""Add notifications for failed DSR requests

Revision ID: 28108b17a99c
Revises: 8f1a19465239
Create Date: 2022-11-07 23:56:14.066374

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "28108b17a99c"
down_revision = "8f1a19465239"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "privacyrequestnotifications",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("notify_after_failures", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_privacyrequestnotifications_id"),
        "privacyrequestnotifications",
        ["id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_privacyrequestnotifications_id"),
        table_name="privacyrequestnotifications",
    )
    op.drop_table("privacyrequestnotifications")
    # ### end Alembic commands ###
