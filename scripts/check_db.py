#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

import aiomysql

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from app.core.config import get_settings


async def check_connection():
    """Check database connection and list available databases"""
    settings = get_settings()
    print("\n=== Database Connection Info ===")
    print(f"Host: {settings.DB_HOST}")
    print(f"Port: {settings.DB_PORT}")
    print(f"User: {settings.DB_USER}")
    print(f"Database: {settings.DB_NAME}")

    conn = None
    specific_conn = None
    try:
        # Try to connect without specifying database first
        conn = await aiomysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
        )

        print("\n✅ Successfully connected to MySQL server")

        async with conn.cursor() as cur:
            # List all databases
            await cur.execute("SHOW DATABASES")
            databases = await cur.fetchall()

            print("\n=== Available Databases ===")
            for db in databases:
                print(f"- {db[0]}")
                if db[0] == settings.DB_NAME:
                    print(f"  ✓ This is your configured database")

        # Now try to connect to the specific database
        try:
            specific_conn = await aiomysql.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                db=settings.DB_NAME,
            )
            print(f"\n✅ Successfully connected to database '{settings.DB_NAME}'")

            # List tables in the database
            async with specific_conn.cursor() as cur:
                await cur.execute("SHOW TABLES")
                tables = await cur.fetchall()

                print("\n=== Tables in Database ===")
                for table in tables:
                    print(f"- {table[0]}")
                    await cur.execute(f"DESCRIBE {table[0]}")
                    columns = await cur.fetchall()
                    print("\n  Table Structure:")
                    for col in columns:
                        print(f"  - {col[0]}: {col[1]}")

        except Exception as e:
            print(f"\n❌ Failed to connect to database '{settings.DB_NAME}'")
            print(f"Error: {str(e)}")
        finally:
            if specific_conn:
                await specific_conn.ensure_closed()

    except Exception as e:
        print("\n❌ Failed to connect to MySQL server")
        print(f"Error: {str(e)}")
    finally:
        if conn:
            await conn.ensure_closed()


if __name__ == "__main__":
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")
    asyncio.run(check_connection())
