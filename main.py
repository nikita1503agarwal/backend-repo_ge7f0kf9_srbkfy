import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Chord, Progression, Lesson, Favorite

app = FastAPI(title="Master Jazz Pianist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Master Jazz Pianist API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# Seed minimal content if empty
@app.post("/seed")
def seed():
    # Seed a few basic chords and a ii-V-I progression if collection empty
    try:
        existing = get_documents("chord", {}, limit=1)
        if not existing:
            create_document("chord", Chord(
                name="C Major 7", symbol="Cmaj7", root="C", quality="major7", notes=["C","E","G","B"],
                extensions=["9","13"], voicings=[["C","E","B","D"],["E","B","D","G"]], tags=["rootless","shell"]
            ))
            create_document("chord", Chord(
                name="G7", symbol="G7", root="G", quality="dominant7", notes=["G","B","D","F"],
                extensions=["9","13"], voicings=[["F","B","E","A"],["B","E","A","D"]], tags=["altered","rootless"]
            ))
            create_document("chord", Chord(
                name="D Minor 7", symbol="Dm7", root="D", quality="minor7", notes=["D","F","A","C"],
                extensions=["9","11"], voicings=[["C","F","A","E"],["F","A","C","E"]], tags=["shell"]
            ))
        existing_prog = get_documents("progression", {}, limit=1)
        if not existing_prog:
            create_document("progression", Progression(
                name="ii-V-I in C", key="C", roman_numerals=["ii","V","I"], chords=["Dm7","G7","Cmaj7"], style="bebop"
            ))
        existing_lesson = get_documents("lesson", {}, limit=1)
        if not existing_lesson:
            create_document("lesson", Lesson(
                title="Rootless ii–V–I Voicings", level="intermediate",
                content="""
### Goal
Play smooth rootless voicings for a ii–V–I in C.

### Steps
- Left hand: keep time with 2 and 4
- Right hand: play Dm9 (C–E–F–A), G13 (F–A–B–E), Cmaj9 (E–A–B–D)
- Practice in all 12 keys using the circle of fifths
""",
                tags=["voicings","ii-v-i","practice"]
            ))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public endpoints
@app.get("/chords")
def list_chords(q: Optional[str] = None):
    try:
        filter_dict = {}
        if q:
            # Simple case-insensitive substring match on name or symbol
            filter_dict = {"$or": [{"name": {"$regex": q, "$options": "i"}}, {"symbol": {"$regex": q, "$options": "i"}}]}
        docs = get_documents("chord", filter_dict)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progressions")
def list_progressions():
    try:
        docs = get_documents("progression")
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lessons")
def list_lessons():
    try:
        docs = get_documents("lesson")
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FavoriteIn(BaseModel):
    client_id: str
    kind: str
    ref: str
    note: Optional[str] = None

@app.post("/favorites")
def add_favorite(fav: FavoriteIn):
    try:
        create_document("favorite", Favorite(**fav.model_dump()))
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/favorites/{client_id}")
def get_favorites(client_id: str):
    try:
        docs = get_documents("favorite", {"client_id": client_id})
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
