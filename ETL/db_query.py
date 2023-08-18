import psycopg2
from psycopg2.extras import DictCursor
from datetime import date


def connect_to_db():
    """
    PostgreSQL DB connections
    :return: Database connection parameters.
    """
    return psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='postgres',
        user='postgres',
        password='postgres'
    )


def insert_data(conn, data):
    """
    Insert the data into user_logins table in the database.
    :param conn: connection parameters
    :param data: dictionary formatted data to store in PostgreSQL database.
    """
    creation_day = date.today()
    postgre_date = creation_day.strftime('%Y-%m-%d')
    # Try except block to confirm the insertion query.
    try:
        # Dictionary formatted data structure for easy retrieval and parameterized query execution.
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            # SQL Query to insert the data into user_logins table.
            cursor.execute(
                """
                    INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, 
                    create_date)
                    VALUES (%(user_id)s, %(device_type)s, %(masked_ip)s, %(masked_device_id)s, %(locale)s, 
                    %(app_version)s, %(create_date)s );
                """,
                {
                    'user_id': data.get('user_id'),
                    'device_type': data.get('device_type', 'DEFAULT_DEVICE_TYPE'),
                    'masked_ip': data.get('masked_ip'),
                    'masked_device_id': data.get('masked_device_id'),
                    'locale': data.get('locale'),
                    'app_version': data.get('app_version'),
                    'create_date': postgre_date
                })
            # print(cursor.execute("SELECT * FROM user_logins"))
        conn.commit()
        print('Data has been inserted successfully.')

    except Exception as exp:
        print(f'Error while inserting the data into the table. {exp}')
