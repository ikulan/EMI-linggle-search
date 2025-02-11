"""
This module contains functions to connect to a PostgreSQL database, create a table, insert data, and query data.
"""
import psycopg2
import re

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="atwolin",
            password="634634634",
            host="localhost",
            port="5432",
            database="linggle_emi",
        )
        return connection
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
        return None


def disconnect_from_db(connection, cursor):
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")


def create_table(connection, cursor, query):
    cursor.execute(query)
    connection.commit()
    print("Table created successfully in PostgreSQL")


def insert_data(connection, cursor, query):
    cursor.execute(query)
    connection.commit()
    print("Data inserted successfully in PostgreSQL")


def function_exists(connection, cursor, function_name):
    query = """
    SELECT EXISTS (
        SELECT 1
        FROM pg_proc
        WHERE proname = %s
    );
    """
    cursor.execute(query, (function_name,))
    return cursor.fetchone()[0]


def create_tsvector(connection, cursor, table_name):
    tsvector_query = f"""ALTER TABLE {table_name} ADD COLUMN tsv_content tsvector;"""
    cursor.execute(tsvector_query)
    update = (
        f"""UPDATE {table_name} SET tsv_content = to_tsvector('english', content);"""
    )
    cursor.execute(update)
    # Trigger function to update tsvector if content is updated
    if not function_exists(connection, cursor, "update_tsv_content"):
        create_function_query = """
            CREATE OR REPLACE FUNCTION update_tsv_content() RETURNS trigger AS $$
            BEGIN
            NEW.tsv_content := to_tsvector('english', NEW.content);
            RETURN NEW;
            END
            $$ LANGUAGE plpgsql;
            """
        cursor.execute(create_function_query)

    # Create the trigger that calls the function before insert or update
    create_trigger_query = f"""
    CREATE TRIGGER tsv_content_trigger
    BEFORE INSERT OR UPDATE ON {table_name}
    FOR EACH ROW EXECUTE FUNCTION update_tsv_content();
    """
    cursor.execute(create_trigger_query)

    # Optimize with indexing
    create_index_query = f"""
        CREATE INDEX IF NOT EXISTS idx_tsv_content ON {table_name} USING GIN(tsv_content);
        """
    cursor.execute(create_index_query)

    connection.commit()
    print("tsvector created successfully in PostgreSQL")


def get_full_text(connection, cursor, table_name, info, search_phrase):
    # search_query = f"""
    # SELECT
    #     {info},
    #     ts_headline('english', content, phraseto_tsquery('english', %s),
    #     'StartSel=<b>, StopSel=</b>, MaxWords = 50, MinWords = 10')
    #     AS snippet

    # FROM {table_name}
    # WHERE tsv_content @@ phraseto_tsquery('english', %s)
    # """
    # cursor.execute(search_query, (search_phrase, search_phrase))
    search_query = f"""
    SELECT
        {info},
        content
    FROM {table_name}
    WHERE content ILIKE %s;
    """
    cursor.execute(search_query, (f"%{search_phrase}%",))

    return cursor.fetchall()


def get_context_around_phrase(text, phrase, num_words=7):
    '''Searches for text, and retrieves `num_words` words either side of the text'''
    # word = r"\W*([\w]+)"
    # groups = re.search(r'{}\W*{}{}'.format(word * num_words, phrase, word * num_words), text)
    partition = text.lower().partition(phrase.lower())
    # print(f"~~~~~~partition[1]: {partition[1]}~~~~~~")
    if partition[1] == "":
        return None
    start_index = partition[0].__len__()
    end_index = start_index + phrase.__len__()
    before = text[:start_index].split()[-num_words:]
    after = text[end_index:].split()[:num_words]
    return " ".join(before) + " <b>" + text[start_index:end_index] + "</b> " + " ".join(after)


def get_partial_text(connection, cursor, table_name, info, search_phrase, limit=3):
    """
    Search for a phrase in the content of the table and return the first `limit` results
    """
    search_query = f"""
    SELECT
        {info},
        content
    FROM {table_name}
    WHERE content ILIKE %s
    LIMIT {limit};
    """
    cursor.execute(search_query, (f"%{search_phrase}%",))
    rows = cursor.fetchall()
    # print(f"Found:\n{rows}\n")

    results = []
    for row in rows:
        if row[-1] is None:
            continue
        # print(f"Before: {row[-1]}")
        context = get_context_around_phrase(row[-1], search_phrase)
        # print(f"After: {context}\n")
        results.append((row[:-1], context))
    return results