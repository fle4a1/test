from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "role" SET DEFAULT 'user';
        ALTER TABLE "users" ALTER COLUMN "password_hash" TYPE BYTEA USING "password_hash"::BYTEA;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "role" SET DEFAULT 'RolesEnum.USER';
        ALTER TABLE "users" ALTER COLUMN "password_hash" TYPE VARCHAR(255) USING "password_hash"::VARCHAR(255);"""
