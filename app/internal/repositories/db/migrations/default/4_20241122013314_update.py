from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    CREATE INDEX IF NOT EXISTS "idx_schedule_professor_search_5f8888" ON schedule USING gin ("professor" gin_trgm_ops);
    CREATE INDEX IF NOT EXISTS "idx_schedule_group_search_5f821d" ON schedule USING gin ("group" gin_trgm_ops);
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
    DROP INDEX IF EXISTS "idx_schedule_group_search_5f821d";
    DROP INDEX IF EXISTS "idx_schedule_professor_search_5f8888";
    DROP EXTENSION IF EXISTS "pg_trgm";
"""
