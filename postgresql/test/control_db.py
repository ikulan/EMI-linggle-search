import psycopg2


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


def full_text_search(connection, cursor, table_name, info, search_phrase):
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
