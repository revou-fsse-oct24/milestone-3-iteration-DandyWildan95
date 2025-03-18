import MySQLdb

try:
    connection = MySQLdb.connect(
        host='localhost',
        user='revobank_user',
        passwd='Bangsat1',
        db='revobank'
    )

    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()

    print(f"MySQL Server Version: {version[0]}")

    connection.close()

except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")