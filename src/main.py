# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
import asyncpg
from pydantic import BaseModel
from typing import List
import joblib
from generate_summary_endpoint import generate_summary_endpoint
import os

dirname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirname)

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5423/my_db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

app = FastAPI()

# Load recommendation model
recommendation_model = joblib.load("../model/recommendation_model.pkl")

# Database models
class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

class Review(BaseModel):
    id: int
    book_id: int
    user_id: int
    review_text: str
    rating: int

@app.post("/books", response_model=Book)
async def add_book(book: Book):
    async with SessionLocal() as session:
        new_book = books.insert().values(
            title=book.title,
            author=book.author,
            genre=book.genre,
            year_published=book.year_published,
            summary=book.summary
        )
        await session.execute(new_book)
        await session.commit()
        return book

@app.get("/books", response_model=List[Book])
async def get_books():
    async with SessionLocal() as session:
        result = await session.execute(select(books))
        books_list = result.scalars().all()
        return books_list

@app.get("/books/{id}", response_model=Book)
async def get_book(id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(books).where(books.c.id == id))
        book = result.scalar()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

@app.put("/books/{id}", response_model=Book)
async def update_book(id: int, book: Book):
    async with SessionLocal() as session:
        query = update(books).where(books.c.id == id).values(
            title=book.title,
            author=book.author,
            genre=book.genre,
            year_published=book.year_published,
            summary=book.summary
        )
        await session.execute(query)
        await session.commit()
        return book

@app.delete("/books/{id}", response_model=Book)
async def delete_book(id: int):
    async with SessionLocal() as session:
        query = delete(books).where(books.c.id == id)
        await session.execute(query)
        await session.commit()
        return {"detail": "Book deleted"}

@app.post("/books/{id}/reviews", response_model=Review)
async def add_review(id: int, review: Review):
    async with SessionLocal() as session:
        new_review = reviews.insert().values(
            book_id=id,
            user_id=review.user_id,
            review_text=review.review_text,
            rating=review.rating
        )
        await session.execute(new_review)
        await session.commit()
        return review

@app.get("/books/{id}/reviews", response_model=List[Review])
async def get_reviews(id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(reviews).where(reviews.c.book_id == id))
        reviews_list = result.scalars().all()
        return reviews_list

@app.get("/books/{id}/summary")
async def get_summary(id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(books).where(books.c.id == id))
        book = result.scalar()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Generate summary using Llama3
        summary = generate_summary(book.summary)
        avg_rating = await session.execute(select(func.avg(reviews.c.rating)).where(reviews.c.book_id == id))
        avg_rating = avg_rating.scalar()
        
        return {"summary": summary, "average_rating": avg_rating}

@app.get("/recommendations")
async def get_recommendations(genre: str, avg_rating: float):
    prediction = recommendation_model.predict([[genre, avg_rating]])
    return {"recommended_book_ids": prediction}
