"""Normalize domain vocabulary and database cascade behavior.

Revision ID: 9b8ea2f7c1d0
Revises: ed333995c455
Create Date: 2026-08-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9b8ea2f7c1d0"
down_revision: str | Sequence[str] | None = "ed333995c455"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "mistake_frequencies",
        "occurances",
        new_column_name="occurrences",
    )
    op.alter_column(
        "mistake_frequencies",
        "category",
        existing_type=sa.Enum("ABC", "DEF", name="mistakecategory"),
        type_=sa.String(length=64),
        postgresql_using=(
            "CASE category::text "
            "WHEN 'ABC' THEN 'subject_verb_agreement' "
            "WHEN 'DEF' THEN 'verb_tense' "
            "ELSE lower(category::text) END"
        ),
    )
    op.execute("DROP TYPE mistakecategory")
    op.create_check_constraint(
        "ck_mistake_frequencies_valid_counts",
        "mistake_frequencies",
        "occurrences >= 0 AND opportunities >= 0 AND occurrences <= opportunities",
    )
    op.drop_constraint("mistake_frequencies_speech_id_fkey", "mistake_frequencies")
    op.create_foreign_key(
        "mistake_frequencies_speech_id_fkey",
        "mistake_frequencies",
        "speeches",
        ["speech_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint("speeches_user_id_fkey", "speeches")
    op.create_foreign_key(
        "speeches_user_id_fkey",
        "speeches",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("speeches_user_id_fkey", "speeches")
    op.create_foreign_key(
        "speeches_user_id_fkey",
        "speeches",
        "users",
        ["user_id"],
        ["id"],
    )
    op.drop_constraint("mistake_frequencies_speech_id_fkey", "mistake_frequencies")
    op.create_foreign_key(
        "mistake_frequencies_speech_id_fkey",
        "mistake_frequencies",
        "speeches",
        ["speech_id"],
        ["id"],
    )
    op.drop_constraint(
        "ck_mistake_frequencies_valid_counts",
        "mistake_frequencies",
        type_="check",
    )
    op.execute("CREATE TYPE mistakecategory AS ENUM ('ABC', 'DEF')")
    op.alter_column(
        "mistake_frequencies",
        "category",
        existing_type=sa.String(length=64),
        type_=sa.Enum("ABC", "DEF", name="mistakecategory"),
        postgresql_using=(
            "CASE category "
            "WHEN 'subject_verb_agreement' THEN 'ABC' "
            "WHEN 'verb_tense' THEN 'DEF' "
            "ELSE 'ABC' END::mistakecategory"
        ),
    )
    op.alter_column(
        "mistake_frequencies",
        "occurrences",
        new_column_name="occurances",
    )
