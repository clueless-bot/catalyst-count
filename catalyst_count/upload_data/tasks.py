import pandas as pd
import os
import asyncio
import asyncpg
import aiofiles
from aiocsv import AsyncReader
from celery import shared_task
from .models import Data

@shared_task
def process_csv_file(file_path):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_csv(file_path))

async def process_csv(file_path):
    chunk_size = 100000  
    conn = await asyncpg.connect(
    user = os.environ.get('DATABASE_USER'),
    password = os.environ.get('DATABASE_PASSWORD'),
    database = os.environ.get('DATABASE_NAME'),
    host = os.environ.get('DATABASE_HOST'),
    )

    async def safe_int(value):
        try:
            return int(value) if value is not None else None
        except (ValueError, TypeError):
            return None

    try:
        async with aiofiles.open(file_path, mode='r') as f:
            reader = AsyncReader(f)
            header = await reader.__anext__()  
            chunk = []
            async for row in reader:
                row_dict = dict(zip(header, row))
                
                year_founded = await safe_int(row_dict.get("year founded"))

                current_employee_estimate = await safe_int(row_dict.get("current employee estimate"))
                total_employee_estimate = await safe_int(row_dict.get("total employee estimate"))

                locality = row_dict.get("locality", "")
                locality_split = locality.split(",") if locality else []
                city = locality_split[0].strip() if len(locality_split) > 0 else None
                state = locality_split[1].strip() if len(locality_split) > 1 else None

                chunk.append(
                    (
                        row_dict["name"] if row_dict["name"] else None,
                        row_dict["domain"] if row_dict["domain"] else None,
                        year_founded,
                        row_dict["industry"] if row_dict["industry"] else None,
                        row_dict["size range"] if row_dict["size range"] else None,
                        row_dict["locality"] if row_dict["locality"] else None,
                        row_dict["country"] if row_dict["country"] else None,
                        row_dict["linkedin url"] if row_dict["linkedin url"] else None,
                        current_employee_estimate,
                        total_employee_estimate,
                        city,
                        state,
                    )
                )

                if len(chunk) >= chunk_size:
                    await insert_chunk(conn, chunk)
                    chunk = []

            if chunk:
                await insert_chunk(conn, chunk)

    except Exception as e:
        print(f"Error occurred: {e}")
        await conn.execute("ROLLBACK;")
        raise
    finally:
        await conn.close()
        os.remove(file_path)

async def insert_chunk(conn, chunk):
    await conn.executemany(
        """
        INSERT INTO upload_data_data (name, domain, year_founded, industry, size_range, locality, country, linkedin_url, current_employee_estimate, total_employee_estimate, city, state)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """,
        chunk
    )