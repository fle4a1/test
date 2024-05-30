from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "schedule";
        CREATE TABLE IF NOT EXISTS "schedule" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "datetime_start" TIMESTAMPTZ NOT NULL,
    "datetime_end" TIMESTAMPTZ NOT NULL,
    "lesson" VARCHAR(150) NOT NULL,
    "professor" VARCHAR(30),
    "type" VARCHAR(20) NOT NULL,
    "subgroup" VARCHAR(1),
    "auditory" VARCHAR(30),
    "group" VARCHAR(30) NOT NULL,
    CONSTRAINT "uid_schedule_datetim_d95386" UNIQUE ("datetime_start", "datetime_end", "lesson", "group")
);
CREATE INDEX IF NOT EXISTS "idx_schedule_group_5f8888" ON "schedule" ("group");
COMMENT ON COLUMN "schedule"."type" IS 'PRACTICE: семинар\nLECTURE: лекции\nLABORATORY: лабораторные занятия';
COMMENT ON COLUMN "schedule"."subgroup" IS 'A: А\nB: Б';
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "schedule";
        CREATE TABLE IF NOT EXISTS "schedule" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "date" DATE NOT NULL,
    "time" VARCHAR(30) NOT NULL,
    "lesson" VARCHAR(150) NOT NULL,
    "professor" VARCHAR(30),
    "type" VARCHAR(20) NOT NULL,
    "subgroup" VARCHAR(1),
    "auditory" VARCHAR(30),
    "group" VARCHAR(30) NOT NULL,
    CONSTRAINT "uid_schedule_date_03f19e" UNIQUE ("date", "time", "lesson", "group")
);
"""
