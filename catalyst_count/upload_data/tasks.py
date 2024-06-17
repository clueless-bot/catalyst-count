from __future__ import absolute_import, unicode_literals
from celery import shared_task
import pandas as pd
import os
import psycopg2
from django.db import transaction
from .models import Data

@shared_task
def process_csv_file(file_path):
    chunk_size = 10000000  # Adjust chunk size as needed

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="catalystdb",
        user="catalyst",
        password="catalyst"
    )

    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            data_to_insert = []
            for _, row in chunk.iterrows():
                year_founded = int(row["year founded"]) if pd.notnull(row["year founded"]) else None

                def safe_int(value):
                    try:
                        return int(value) if pd.notnull(value) else None
                    except (ValueError, TypeError):
                        return None

                current_employee_estimate = safe_int(row.get("current employee estimate", "0"))
                total_employee_estimate = safe_int(row.get("total employee estimate", "0"))

                locality = row.get("locality", "")
                locality_split = locality.split(",") if pd.notnull(locality) else []
                city = locality_split[0].strip() if len(locality_split) > 0 else None
                state = locality_split[1].strip() if len(locality_split) > 1 else None

                data_to_insert.append(
                    (
                        row["name"] if pd.notnull(row["name"]) else None,
                        row["domain"] if pd.notnull(row["domain"]) else None,
                        year_founded,
                        row["industry"] if pd.notnull(row["industry"]) else None,
                        row["size range"] if pd.notnull(row["size range"]) else None,
                        row["locality"] if pd.notnull(row["locality"]) else None,
                        row["country"] if pd.notnull(row["country"]) else None,
                        row["linkedin url"] if pd.notnull(row["linkedin url"]) else None,
                        current_employee_estimate,
                        total_employee_estimate,
                        city,
                        state,
                    )
                )

            # Insert data in chunks using raw SQL
            with conn.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO upload_data_data (name, domain, year_founded, industry, size_range, locality, country, linkedin_url, current_employee_estimate, total_employee_estimate, city, state)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    data_to_insert
                )
            conn.commit()  # Commit the transaction after each chunk

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()  # Rollback the transaction in case of error
        raise
    finally:
        conn.close()  # Close the database connection

    os.remove(file_path)  # Remove the file after processing
