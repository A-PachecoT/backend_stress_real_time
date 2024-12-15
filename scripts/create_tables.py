import asyncio

import aiomysql

from app.core.config import get_settings

settings = get_settings()

DROP_QUESTION_RESPONSES_TABLE = """
DROP TABLE IF EXISTS question_responses;
"""

DROP_USERS_TABLE = """
DROP TABLE IF EXISTS users;
"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    full_name VARCHAR(150) NULL,
    age INTEGER NULL,
    gender VARCHAR(20) NULL,
    marital_status VARCHAR(20) NULL,
    occupation VARCHAR(100) NULL,
    PRIMARY KEY (id),
    UNIQUE (username),
    UNIQUE (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

CREATE_QUESTION_RESPONSES_TABLE = """
CREATE TABLE IF NOT EXISTS question_responses (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    question_number INTEGER NOT NULL,
    answer_value INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_question (user_id, question_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


async def recreate_tables():
    conn = await aiomysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        db=settings.DB_NAME,
    )

    async with conn.cursor() as cur:
        try:
            # Drop existing tables (in correct order due to foreign key)
            await cur.execute(DROP_QUESTION_RESPONSES_TABLE)
            print("🗑️ Question responses table dropped successfully!")

            await cur.execute(DROP_USERS_TABLE)
            print("🗑️ Users table dropped successfully!")

            # Create tables (in correct order for foreign keys)
            await cur.execute(CREATE_USERS_TABLE)
            print("✅ Users table created successfully!")

            await cur.execute(CREATE_QUESTION_RESPONSES_TABLE)
            await conn.commit()
            print("✅ Question responses table created successfully!")
        except Exception as e:
            print(f"❌ Error recreating tables: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    asyncio.run(recreate_tables())
