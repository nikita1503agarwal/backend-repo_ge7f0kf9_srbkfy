"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Jazz Mastery app schemas

class Chord(BaseModel):
    """
    Chords collection schema
    Collection name: "chord"
    """
    name: str = Field(..., description="Human-readable name, e.g., C Major 7")
    symbol: str = Field(..., description="Symbol, e.g., Cmaj7, Fm9, G7b9")
    root: str = Field(..., description="Root note, e.g., C, F#, Bb")
    quality: str = Field(..., description="Quality, e.g., major7, minor7, dominant7, diminished, altered")
    notes: List[str] = Field(..., description="List of pitch classes in ascending order, e.g., ['C','E','G','B']")
    extensions: Optional[List[str]] = Field(default=None, description="Optional extensions, e.g., ['9','#11','13']")
    voicings: Optional[List[List[str]]] = Field(default=None, description="Common piano voicings, each a list of notes, low-to-high")
    tags: Optional[List[str]] = Field(default=None, description="Tags like 'shell', 'quartal', 'left-hand', 'rootless'")

class Progression(BaseModel):
    """
    Progressions collection schema
    Collection name: "progression"
    """
    name: str = Field(..., description="Name of progression, e.g., 2-5-1 in C")
    key: str = Field(..., description="Key center, e.g., C, F#, Bb")
    roman_numerals: List[str] = Field(..., description="Roman numerals, e.g., ['ii','V','I']")
    chords: List[str] = Field(..., description="Chord symbols in order, e.g., ['Dm7','G7','Cmaj7']")
    style: Optional[str] = Field(default=None, description="Style or context, e.g., bebop, modal, blues")

class Lesson(BaseModel):
    """
    Lessons collection schema
    Collection name: "lesson"
    """
    title: str
    level: str = Field(..., description="beginner | intermediate | advanced")
    content: str = Field(..., description="Markdown content for the lesson body")
    tags: Optional[List[str]] = Field(default=None)

class Favorite(BaseModel):
    """
    Favorites collection schema
    Collection name: "favorite"
    """
    client_id: str = Field(..., description="Anonymous client identifier from frontend")
    kind: str = Field(..., description="'chord' or 'progression'")
    ref: str = Field(..., description="Referenced symbol or name (for simplicity)")
    note: Optional[str] = Field(default=None, description="Optional note or label")

# Example schemas (kept for reference)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
