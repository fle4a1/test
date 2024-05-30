from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(30) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "role" VARCHAR(5) NOT NULL  DEFAULT 'user'
);
COMMENT ON COLUMN "users"."role" IS 'USER: user\nADMIN: admin';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "users";"""
