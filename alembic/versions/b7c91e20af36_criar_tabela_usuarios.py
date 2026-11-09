"""Cria a tabela de usuários."""

import sqlalchemy as sa
from alembic import op

revision = "b7c91e20af36"
down_revision = "4e9d8bea2c94"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(254), nullable=False, unique=True),
        sa.Column("senha_hash", sa.String(255), nullable=False),
    )


def downgrade():
    op.drop_table("usuarios")
