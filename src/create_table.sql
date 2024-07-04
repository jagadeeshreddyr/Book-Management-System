-- books table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    year_published INT,
    summary TEXT
);

-- reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_id INT REFERENCES books(id),
    user_id INT,
    review_text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5)
);
