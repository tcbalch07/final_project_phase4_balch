## Bookstore Web Application
This is a web application for managing and exploring a bookstore. 
It allows users to browse, filter, and visualize books and reviews and offers 
CRUD functionality. The application is built with Flask and includes features 
like dynamic visualizations and comprehensive search filters.

## Features
- Full CRUD functionality for books and reviews.
- Dynamic filtering by:
      Price range.
      Ratings (1-5 stars).
-Interactive visualizations using Plotly to explore:
      Popular books based on reviews.
      Average ratings of books.
-User-friendly design with Bootstrap for responsive layouts.

## Novel Feature: Visualizations & Dynamic Filtering
The visualizations allow users to explore data about books and reviews, making the data 
more accessible. For example: The Popular Books chart highlights books with the highest number of reviews.
The Average Ratings visualization provides insights into the most highly-rated books.
This feature was chosen because it transforms raw information into insights, 
allowing users to quickly identify trends such as popular or highly-rated books without 
manually sorting through data. The dynamic filtering feature allows users to narrow down 
their search results based on price range and ratings, making it easier to find books that meet their criteria.
It was chosen because it enhances the user experience by providing a more personalized and efficient way to search for books.

## Technologies Used
- Flask: Backend framework for handling routes and database connections.
- SQLite: Lightweight database for storing books and reviews.
- Plotly: Library for creating interactive visualizations.
- Bootstrap: For responsive and user-friendly UI.
- Python Libraries: pymysql, Jinja2, and others.
