import psycopg2

def fetch_and_print_all_items():
    # Database connection parameters
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'vagrant',
        'host': 'localhost',
        'port': 5432           # the port mapped in runpostgres.sh script
    }

    # SQL query to select all items
    query = "SELECT * FROM property_listings;"  # replace with your table name

    # Connect to the database
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the table
        rows = cursor.fetchall()

        # Print each row
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print("An error occurred:", e)

fetch_and_print_all_items()
