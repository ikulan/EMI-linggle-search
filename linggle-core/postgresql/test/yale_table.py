"""
To create a PostgreSQL table for Yale OCW data and store the data in the table
"""
import os
from pprint import pprint

from control_db import *

connection = connect_to_db()
cursor = connection.cursor()


def create_yale_table():
    create_table_query = """CREATE TABLE yale (
        id SERIAL PRIMARY KEY,             -- Auto-increment primary key
        course_name VARCHAR(255) NOT NULL, -- Course name (e.g., african-american-studies)
        sub_course_name VARCHAR(255) NOT NULL, -- Sub-course name (e.g., AFAM-162)
        file_name VARCHAR(255) NOT NULL,   -- File name (e.g., lecture_1.txt)
        content TEXT NOT NULL              -- Contents of the text file
    );"""
    create_table(connection, cursor, create_table_query)


def store_yale_data(id, course_name, sub_course_name, file_name, content):
    # Insert data into the table
    insert_data_query = f"""INSERT INTO yale (id, course_name, sub_course_name, file_name, content)
        VALUES ('{id}', '{course_name}', '{sub_course_name}', '{file_name}', '{content}');"""
    insert_data(connection, cursor, insert_data_query)


def process_files(root_dir):
    """
    Process all files in the Yale OCW directory and store in the database
    """
    id = 0
    for course_name in os.listdir(root_dir):
        course_dir = os.path.join(root_dir, course_name)
        if os.path.isdir(course_dir):
            for sub_course_name in os.listdir(course_dir):
                sub_course_dir = os.path.join(course_dir, sub_course_name)
                if os.path.isdir(sub_course_dir):
                    for file_name in os.listdir(sub_course_dir):
                        file_path = os.path.join(sub_course_dir, file_name)
                        if file_name.endswith(".txt"):
                            with open(file_path, "r") as file:
                                if id == 10:
                                    break
                                content = file.read()
                                print(
                                    f"Data: {course_name}/{sub_course_name}/{file_name}"
                                )
                                store_yale_data(
                                    id, course_name, sub_course_name, file_name, content
                                )
                                id += 1

                                # print(f"Data stored for {course_name}/{sub_course_name}/{file_name}")


def fetch_one_row():

    cursor.execute("SELECT * FROM yale;")
    row = cursor.fetchone()
    pprint(row)


if __name__ == "__main__":

    # Prepare the database
    # create_yale_table(connection, cursor)

    # root_dir = "/home/nlplab/atwolin/EMI-linggle-search/yale-ocw"
    # process_files(root_dir)
    # create_tsvector(connection, cursor, "yale")  # Create tsvector for full-text search

    # Start searching
    info = "course_name, sub_course_name, file_name"
    search_phrase = "Civil Rights Movement"
    # results = get_full_text(connection, cursor, "yale", info, search_phrase)
    results = get_partial_text(connection, cursor, "yale", info, search_phrase)
    for row in results:
        print(row)

    disconnect_from_db(connection, cursor)
