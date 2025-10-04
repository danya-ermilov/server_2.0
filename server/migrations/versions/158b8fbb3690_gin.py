"""gin

Revision ID: 158b8fbb3690
Revises: e93c2d464b8b
Create Date: 2025-08-28 21:33:37.616407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '158b8fbb3690'
down_revision: Union[str, Sequence[str], None] = 'e93c2d464b8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TABLE products ADD COLUMN search_vector tsvector")

    op.execute("UPDATE products SET search_vector = to_tsvector('simple', coalesce(name,'') || ' ' || coalesce(description,''))")

    op.execute("CREATE INDEX products_search_idx ON products USING GIN (search_vector)")

    op.execute("""
    CREATE FUNCTION products_tsvector_trigger() RETURNS trigger AS $$
    begin
      new.search_vector := to_tsvector('simple', coalesce(new.name,'') || ' ' || coalesce(new.description,''));
      return new;
    end
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON products FOR EACH ROW EXECUTE FUNCTION products_tsvector_trigger();
    """)

def downgrade():
    op.execute("DROP TRIGGER tsvectorupdate ON products")
    op.execute("DROP FUNCTION products_tsvector_trigger")
    op.execute("DROP INDEX products_search_idx")
    op.execute("ALTER TABLE products DROP COLUMN search_vector")