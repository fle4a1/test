from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
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
CREATE INDEX IF NOT EXISTS "idx_schedule_date_050b56" ON "schedule" ("date");
CREATE INDEX IF NOT EXISTS "idx_schedule_group_5f8888" ON "schedule" ("group");
COMMENT ON COLUMN "schedule"."type" IS 'PRACTICE: семинар\nLECTURE: лекции\nLABORATORY: лабораторные занятия';
COMMENT ON COLUMN "schedule"."subgroup" IS 'A: А\nB: Б';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
