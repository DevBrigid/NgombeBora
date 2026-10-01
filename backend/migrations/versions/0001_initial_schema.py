"""Create the initial NgombeBora schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("cows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("serial_number", sa.String(80), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("breed", sa.String(100)), sa.Column("sex", sa.String(10), nullable=False),
        sa.Column("date_of_birth", sa.Date()), sa.Column("birth_weight", sa.Numeric(8, 2)),
        sa.Column("acquisition_type", sa.String(12), nullable=False),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("mother_id", sa.Integer()), sa.Column("sire_id", sa.Integer()),
        sa.Column("sire_external", sa.String(160)), sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("sex IN ('male','female')", name="ck_cow_sex"),
        sa.CheckConstraint("acquisition_type IN ('born','purchased')", name="ck_cow_acquisition"),
        sa.CheckConstraint("status IN ('active','sold','deceased')", name="ck_cow_status"),
        sa.CheckConstraint("NOT (sire_id IS NOT NULL AND sire_external IS NOT NULL)", name="ck_cow_single_sire"),
        sa.ForeignKeyConstraint(["mother_id"], ["cows.id"]),
        sa.ForeignKeyConstraint(["sire_id"], ["cows.id"]), sa.UniqueConstraint("serial_number"))
    op.create_index("ix_cows_serial_number", "cows", ["serial_number"])
    op.create_table("milk_records",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("date", sa.Date(), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 2), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_milk_records_date", "milk_records", ["date"])
    op.create_table("finance_entries",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("date", sa.Date(), nullable=False),
        sa.Column("type", sa.String(12), nullable=False), sa.Column("category", sa.String(40), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False), sa.Column("note", sa.String(500)),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("type IN ('income','expenditure')", name="ck_finance_type"))
    op.create_index("ix_finance_entries_date", "finance_entries", ["date"])


def downgrade():
    op.drop_index("ix_finance_entries_date", table_name="finance_entries")
    op.drop_table("finance_entries")
    op.drop_index("ix_milk_records_date", table_name="milk_records")
    op.drop_table("milk_records")
    op.drop_index("ix_cows_serial_number", table_name="cows")
    op.drop_table("cows")
