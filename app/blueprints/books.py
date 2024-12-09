from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db
import pymysql

books_bp = Blueprint('books', __name__)

@books_bp.route('/catalog', methods=['GET', 'POST'])
def catalog():
    db = get_db()
    cursor = db.cursor()

    # Query to fetch all book titles for the dropdown
    cursor.execute("SELECT books_id, title FROM books")
    all_books = cursor.fetchall()

    # Get filter parameters from the request
    book_id_filter = request.args.get('book_id')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_rating = request.args.get('min_rating')
    max_rating = request.args.get('max_rating')

    # Base query with optional WHERE and HAVING clauses
    query = """
        SELECT b.books_id, b.title, b.author, b.price, b.description, AVG(r.rating) AS avg_rating
        FROM books b
        LEFT JOIN reviews r ON b.books_id = r.book_id
    """
    where_clauses = []
    having_clauses = []
    params = []

    # Filters for WHERE clause
    if book_id_filter:
        where_clauses.append("b.books_id = %s")
        params.append(book_id_filter)
    if min_price:
        where_clauses.append("b.price >= %s")
        params.append(min_price)
    if max_price:
        where_clauses.append("b.price <= %s")
        params.append(max_price)

    # Filters for HAVING clause
    if min_rating:
        having_clauses.append("AVG(r.rating) >= %s")
        params.append(min_rating)
    if max_rating:
        having_clauses.append("AVG(r.rating) <= %s")
        params.append(max_rating)

    # Combine WHERE clause
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    # Grouping and HAVING clause
    query += " GROUP BY b.books_id"
    if having_clauses:
        query += " HAVING " + " AND ".join(having_clauses)

    # Execute the query with parameters
    cursor.execute(query, params)
    books = cursor.fetchall()

    cursor.close()
    db.close()

    # Pass books and all_books (for dropdown) to the template
    return render_template('catalog.html', books=books, all_books=all_books)

@books_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        description = request.form['description']  # Added description field

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO books (title, author, price, description) VALUES (%s, %s, %s, %s)", (title, author, price, description))  # Added description here
        db.commit()
        flash('Book added successfully!')
        return redirect(url_for('books.catalog'))
    return render_template('add_book.html')

@books_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    # Your logic to edit the book details
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM books WHERE books_id = %s", (book_id,))
    book = cursor.fetchone()

    if request.method == 'POST':
        # Your logic to update the book in the database
        cursor.execute("UPDATE books SET title = %s, author = %s, price = %s, description = %s WHERE books_id = %s",
                       (request.form['title'], request.form['author'], request.form['price'], request.form['description'], book_id))  # Updated with description
        get_db().commit()
        return redirect(url_for('books.catalog'))  # Redirect back to catalog page

    return render_template('update_book.html', book=book)

@books_bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    try:
        # First, delete the reviews related to the book
        cursor.execute("DELETE FROM reviews WHERE book_id = %s", (book_id,))
        db.commit()

        # Then, delete the book itself
        cursor.execute("DELETE FROM books WHERE books_id = %s", (book_id,))
        db.commit()

        flash('Book and associated reviews deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('books.catalog'))


@books_bp.route('/review/<int:book_id>', methods=['POST'])
def add_review(book_id):
    review = request.form['review']
    rating = request.form['rating']

    db = get_db()
    cursor = db.cursor()

    # Insert the review into the reviews table
    cursor.execute("INSERT INTO reviews (book_id, review_text, rating) VALUES (%s, %s, %s)", (book_id, review, rating))
    db.commit()

    flash('Review added successfully!')
    return redirect(url_for('books.book_details', book_id=book_id))  # Redirect to the book's detail page


@books_bp.route('/book_details/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    connection = get_db()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to return dictionaries

    # Query for the book details
    cursor.execute("SELECT * FROM books WHERE books_id = %s", (book_id,))
    book = cursor.fetchone()

    # Query for the reviews for this book (use review_text instead of review)
    cursor.execute("SELECT * FROM reviews WHERE book_id = %s", (book_id,))
    reviews = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    return render_template('book_details.html', book=book, reviews=reviews)

@books_bp.route('/events', methods=['GET', 'POST'])
def events():
    return render_template('events.html')


@books_bp.route('/api/popular_books', methods=['GET'])
def popular_books():
    db = get_db()
    cursor = db.cursor()

    # Query to fetch books with review counts and average ratings
    cursor.execute("""
        SELECT b.title, COUNT(r.review_id) AS review_count, AVG(r.rating) AS avg_rating
        FROM books b
        LEFT JOIN reviews r ON b.books_id = r.book_id
        GROUP BY b.books_id
        ORDER BY review_count DESC, avg_rating DESC
        LIMIT 10
    """)
    books = cursor.fetchall()
    cursor.close()
    db.close()

    # Return the data as JSON
    return jsonify(books)

@books_bp.route('/visualizations', methods=['GET'])
def visualizations():
    return render_template('visualizations.html')

