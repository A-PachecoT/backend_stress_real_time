#!/usr/bin/env python3
import asyncio
import os
from datetime import datetime
from pathlib import Path

import aiomysql
from tabulate import tabulate

from app.core.config import get_settings

settings = get_settings()


async def show_table_content(table_name: str):
    """Display content of a specific table"""
    conn = None
    try:
        conn = await aiomysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME,
        )

        async with conn.cursor() as cur:
            # Get column names
            await cur.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in await cur.fetchall()]

            # Get data
            await cur.execute(f"SELECT * FROM {table_name}")
            rows = await cur.fetchall()

            # Print table
            print(f"\n=== Content of {table_name} ===")
            print(tabulate(rows, headers=columns, tablefmt="grid"))
            print(f"Total rows: {len(rows)}")

    except Exception as e:
        print(f"\n❌ Error accessing table {table_name}")
        print(f"Error: {str(e)}")
    finally:
        if conn:
            await conn.ensure_closed()


async def main():
    """Main function to show database content"""
    tables = ["users", "sensores", "question_responses"]

    for table in tables:
        await show_table_content(table)


if __name__ == "__main__":
    print("=== Database Content Viewer ===")
    print(f"Database: {settings.DB_NAME}")
    print(f"Host: {settings.DB_HOST}")
    asyncio.run(main())
