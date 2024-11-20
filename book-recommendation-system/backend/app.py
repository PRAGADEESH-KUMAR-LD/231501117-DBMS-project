from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from database import get_db_connection
from models import Book

app = Flask(__name__)
CORS(app)

# Helper function to apply search and sorting
def apply_filters_and_sorting(query, params):
    search_term = params.get('search', None)
    sort_by = params.get('sort_by', 'avg_rating')
    sort_order = params.get('order', 'asc')
    
    # Apply search filter if search term is provided
    if search_term:
        query += " WHERE title LIKE %s OR author LIKE %s OR genres LIKE %s"
        # Use params as a list instead of a dict to avoid the AttributeError
        params_list = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']
    else:
        params_list = []
    
    # Apply sorting
    if sort_by and sort_order:
        query += f" ORDER BY {sort_by} {sort_order.upper()}"
    
    # Return the query and the list of parameters for executing the query
    return query, params_list


@app.route('/')
def home():
    return render_template('index.html')


# Check that the API returns all necessary fields
@app.route('/books', methods=['GET'])
def get_books():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Base query to select all books
    query = 'SELECT * FROM books'
    params = []

    # Apply search and sorting based on URL query parameters
    query, params = apply_filters_and_sorting(query, request.args.to_dict())

    # Pagination: Handle 'page' and 'page_size' parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    offset = (page - 1) * page_size
    query += f" LIMIT {page_size} OFFSET {offset}"

    cursor.execute(query, params)
    books_data = cursor.fetchall()

    # Get total number of books for pagination
    cursor.execute("SELECT COUNT(*) AS total FROM books")
    total_books = cursor.fetchone()['total']

    connection.close()

    books = []
    for book in books_data:
        books.append({
            'title': book['title'],
            'author': book['author'],
            'description': book['description'],
            'genres': book['genres'],
            'avg_rating': book['avg_rating'],
            'num_ratings': book['num_ratings'],
            'url': book['url']
        })

    return jsonify({'books': books, 'totalBooks': total_books})



if __name__ == '__main__':
    app.run(debug=True)
