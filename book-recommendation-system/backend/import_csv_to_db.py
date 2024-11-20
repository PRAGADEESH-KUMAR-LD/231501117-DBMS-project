import csv
import mysql.connector

def import_csv_to_db():
    with open('books.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',               # Replace with your DB user
            password='pragadeeshluck2005',     # Replace with your DB password
            database='book_recommendation'
        )
        cursor = connection.cursor()

        for row in reader:
            # Ensure Num_Ratings is an integer or default to 0 if invalid
            Num_Ratings = row['Num_Ratings']
            try:
                Num_Ratings = int(Num_Ratings)
            except ValueError:
                Num_Ratings = 0  # default to 0 if the value is invalid

            cursor.execute("""
                INSERT INTO books (title, author, description, genres, avg_rating, Num_Ratings, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['Title'],         # Adjust according to CSV column names
                row['Author'],        # Adjust according to CSV column names
                row['Description'],   # Adjust according to CSV column names
                row['Genres'],        # Adjust according to CSV column names
                row['Avg_Rating'],    # Adjust according to CSV column names
                Num_Ratings,          # Ensure it's an integer
                row['URL']            # Adjust according to CSV column names
            ))

        connection.commit()
        connection.close()
        print("CSV data imported successfully!")

if __name__ == "__main__":
    import_csv_to_db()
