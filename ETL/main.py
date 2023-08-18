import json
from sqs_client import create_sqs_client, retrieve_messages
from etl_process import transform_data
from db_query import connect_to_db, insert_data


def main():
    # create SQS client
    client = create_sqs_client()

    # SQS URL
    sqs_url = "http://localhost:4566/000000000000/login-queue"

    # Database connection
    conn = connect_to_db()

    message = retrieve_messages(client, sqs_url)

    if message is not None:
        # Parse message body to insert in database from the JSON input.
        message_body = json.loads(message['Body'])
        # Implement masking and transformation on the message body.
        transformed_data = transform_data(message_body)
        # Insert the data into the database.
        insert_data(conn, transformed_data)

    conn.close()


if __name__ == "__main__":
    main()
