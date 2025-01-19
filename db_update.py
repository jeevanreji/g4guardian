import mysql.connector
import time

# MySQL DB connection configuration
DB_CONFIG = {
    'user': 'admin',    # Update with your DB username
    'password': 'Realmadrid123',  # Update with your DB password
    'host': 'database-1-instance-1.cxq6e0c880zp.us-east-1.rds.amazonaws.com',         # Update with your DB host, might be an IP address
    'database': 'database-1'  # Update with your DB name
}

def get_db_connection():
    """
    Helper function to establish a connection to the MySQL database.
    """
    return mysql.connector.connect(
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database']
    )

def check_and_update_entries():
    """
    Checks entries in the database where a specific condition is met and updates a column.
    """
    # Get a DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        while True:
            # Select entries that are not 'master' from a particular column
            cursor.execute("SELECT id, energy_demand,energy_consumed FROM user WHERE role != 'master'")
            rows = cursor.fetchall()

            if rows:
                print(f"Found {len(rows)} rows to update")

                # Loop over the rows and update the relevant column
                for row in rows:
                    row_id = row[0]  # Assuming id is in the first column
                    print(f"Updating row {row_id}")

                    # Example: Update a particular column (say `status_column`)
                    cursor.execute("UPDATE user SET energy_consumed = energy_consumed + energy_demand WHERE id = %s", (row_id,))

                
                # Commit changes
                connection.commit()
                print("Changes committed successfully")

            else:
                print("No rows found to update")

            # Wait for 30 seconds before checking again
            time.sleep(60)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    check_and_update_entries()
