# Fetch Rewards Data Engineering ETL Challenge 

I've developed a Python script that retrieves information from an AWS Simple Queue Service (SQS), applies data masking and other crucial transformations, and subsequently saves the processed data into a PostgreSQL database.


### Setup:

#### Prerequisites


1. [Python 3.8.6](https://www.python.org/downloads/release/python-386/): 

2. [Docker](https://docs.docker.com/get-docker/ )

3. Docker Compose:
    - Windows and macOS: Comes pre-installed with Docker.
    - Linux: [guide](https://docs.docker.com/compose/install/).

4. [AWS CLI](https://aws.amazon.com/cli/)
 
5. AWS CLI Local : 
    ```
    pip install awscli-local
    ```
    Configure AWS credentials for Localstack can be dummy as mentioned below:

    ```
    aws configure
    ```
    
    ```
    AWS Access Key ID [None]: test
    AWS Secret Access Key [None]: test
    Default region name [None]: us-east-1
    Default output format [None]: json
    ```

6. Clone the Repository, 
    Run the following command to clone repository:
    ```
   git@github.com:simants/ETL_Fetch_DE.git
   ```
      File structure is as follows:
   1. ETL directory consist four python scripts:
      1. `db_query.py`: Contains database connection configuration and insertion query.
      2. `etl_process.py`: Scripts for encryption-decryption and data transformation.
      3. `sql_client.py`: Script for extracting data from AWS Simple Queue Service( SQS)
      4. `main.py`: Main file to execute the program.
   2. `docker-compose.yml`: Consist of docker configuration. 
   3. `requirements.txt`: All the requirements to execute the project.
   4. `variables.py`: Stores generated encryption key.

    
7. Install all the Python packages in the requirements.txt file.
      Run Command:
       ```
       pip install -r requirements.txt
       ```

## Start the docker container services

You need to start docker for PostgresSQL database to be up and Localstack:

```
docker-compose up
```


### Check AWS Localstack Running
Check the Localstack service is up using AWS CLI Local in new terminal. Run command:

```
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
```
This command will output JSON response representing a following message from the queue:
```
{
    "Messages": [
        {
            "MessageId": "3c007da8-3ca5-4df6-8a78-9b0162d7db3b",
            "ReceiptHandle": "ODkxNmU3MmYtYzA1YS00NTk0LThkMDMtNGVlYjc3ZDdjMTA0IGFybjphd3M6c3FzOnVzLWVhc3QtMTowMDAwMDAwMDAwMDA6bG9naW4tcXVldWUgM2MwMDdkYTgtM2NhNS00ZGY2LThhNzgtOWIwMTYyZDdkYjNiIDE2OTEyNzE3NTQuOTc1NDQ2Nw==",
            "MD5OfBody": "e4f1de8c099c0acd7cb05ba9e790ac02",
            "Body": "{\"user_id\": \"424cdd21-063a-43a7-b91b-7ca1a833afae\", \"app_version\": \"2.3.0\", \"device_type\": \"android\", \"ip\": \"199.172.111.135\", \"locale\": \"RU\", \"device_id\": \"593-47-5928\"}"
        }
    ]
}

```
### Verify the table contains 

```
psql -d postgres -U postgres -p 5432 -h localhost -W
```
Enter password : 
```
postgres
```
Execute Query:
```
SELECT * FROM user_logins;
```
user_logins table should be empty:

```
 user_id | device_type | masked_ip | masked_device_id | locale | app_version | create_date 
---------+-------------+-----------+------------------+--------+-------------+-------------
(0 rows)

```
#### Exit PostgreSQL prompt, using 
```
\q
```
and press enter key.

## Project Execution

Navigate to `/ETL` directory in the project folder and run `main.py` file. 

This file will perform following operations:
1. Extract Data form Amazon Simple Queue Service(SQS)
2. Perform masking on Personal Identifiable Information(PII).
3. Transform the data to flatten json data.
4. Insert data into 'user_logins' table.

Run following command:

Navigate to the ETL directory from ETL_Fetch_DE project folder:
```
cd /{your file folder path}/ETL_Fetch_DE/ETL
```
Execute project using command:

```
python main.py
```
If the insertion was successful terminal will print the following output:

_**'Data has been inserted successfully.'**_

else it will print the exception raised.


## Verify successful insertion of data in PostgreSQL database

Connect to PostgreSQl database by running following psql command in terminal
```
psql -d postgres -U postgres -p 5432 -h localhost -W
```
Enter password : 
```
postgres
```

#### Execute select query to display records in the user_logins table.

```
SELECT * FROM user_logins;
```
You should see the records of the user_logins table, something like this:
```
               user_id                | device_type |            masked_ip             |         masked_device_id         | locale | app_version | create_date 
--------------------------------------+-------------+----------------------------------+----------------------------------+--------+-------------+-------------
 424cdd21-063a-43a7-b91b-7ca1a833afae | android     | gAAAAABk39TSPIwUfGEKVCC777kVCp0juRqTFPa5HnOdhIZctsBeGAV5o38gvM-fVW1YuXPL9Y1qvlGZVr7DKTuC7oUxoIJMOA== | gAAAAABk39TS3MqUTCaLdGJBdxwLsjHI2CIdxbnSuPh8AU1iZPp7I4qaF9508PF8SrqYKnCrbf7XcJTkK_ijWnsBaPx7MJx7sg== | RU     |         230 | 
(1 row)

```
#### Exit PostgreSQL prompt, using 
```
\q
```
and press enter key.

### Stop running Containers:

```
docker-compose down
```


## Design Decisions
#### How will you read messages from the queue?
- Employed boto3 client to interface with AWS SQS. Messages are retrieved in sequential pattern, transformation are implied and then further stored in PostgreSQL.
#### What type of data structures should be used?
- The utilization of a dictionary data structure harmonizes seamlessly with JSON-formatted data, which follows a key-value paradigm. This structure has been employed to store data retrieved from AWS SQS, facilitating effortless data retrieval and efficient lookup operations. 
#### How will you mask the PII data so that duplicate values can be identified?
- In order to enhance data privacy measures, we have integrated Fernet symmetric encryption from the cryptography library. This encryption technique is applied to the ip and device_id fields. This approach guarantees that the underlying data is transformed into an encrypted format, maintaining a predictable encrypted output for matching inputs. This predictable behavior is essential for the identification of duplicate records, even following the data masking process.
#### What will be your strategy for connecting and writing to Postgres?
- The project utilizes the psycopg2 library to engage with the PostgreSQL database. The establishment of connections and data insertion is facilitated through the db_query.py file. The utilization of DictCursor streamlines parameter binding, while data integrity is ensured through the commit function, which maintains transaction durability. In case of any issues during data insertion, exceptions are managed within an exception block for enhanced robustness.
#### Where and how will your application run?
- A local development environment should be equipped with essential software such as Python, PostgreSQL, and their respective dependencies. Containerization can be employed for consistent deployment across diverse environments.
## Additional Questions
#### How would you deploy this application in production?
- Ensure the implementation of secret management and user access profiling mechanisms to restrict data and secret key access exclusively to authorized users. Additionally, encapsulating this application within a Docker container guarantees dependable and uniform deployments across diverse environments, as highlighted earlier.

#### What other components would you want to add to make this production ready?
- We affirm the application's production readiness due to its loosely coupled services. Different functions are organized into separate files, enhancing issue detection. Comprehensive exception handling is in place during insertion and data retrieval processes, ensuring robustness. Data quality checks address empty fields in retrieved data, ensuring readiness for production deployment.
#### How can this application scale with a growing dataset.
- Leveraging AWS SQS offers high scalability. Retrieving messages from SQS can be seamlessly scaled based on demand. As the images are hosted in Docker containers, this program can be executed across multiple machines, enabling scalability in handling larger datasets. Further scalability is achieved by deploying the application on cloud or container platforms.
#### How can PII be recovered later on?
- Personal Identifiable Information (PII) recovery is facilitated by the decrypt function, utilizing the Fernet symmetric encryption. Controlled access to the key value in variables.py is vital, requiring proper authorization for viewing.

#### What are the assumptions you made?
- Implemented within the system is a single-key encryption mechanism, based on the assumption that each user_id is associated with a unique mapping of ip and device_id. The retrieved data adheres to the database schema's data type. The system is designed to operate with a dependable and persistent connection.