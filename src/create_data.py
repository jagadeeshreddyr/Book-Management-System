# generate_synthetic_data.py
import pandas as pd
import numpy as np
import os

dirname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirname)

# Parameters for synthetic data
num_books = 1000
genres = ['Fiction', 'Non-Fiction', 'Mystery', 'Science Fiction', 'Fantasy', 'Biography']
authors = ['Author A', 'Author B', 'Author C', 'Author D', 'Author E']
titles = [f'Book {i}' for i in range(1, num_books + 1)]

# Generate synthetic data
np.random.seed(42)
data = {
    'book_id': range(1, num_books + 1),
    'title': np.random.choice(titles, num_books, replace=False),
    'author': np.random.choice(authors, num_books),
    'genre': np.random.choice(genres, num_books),
    'average_rating': np.random.uniform(1, 5, num_books).round(2)
}

# Create DataFrame
books_df = pd.DataFrame(data)

# Save to CSV
books_df.to_csv("../data/books_dataset.csv", index=False)

