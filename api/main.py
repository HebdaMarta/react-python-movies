from fastapi import FastAPI, Body, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Any
import sqlite3

class Movie(BaseModel):
    title: str
    year: str
    actors: list[str] = []

app = FastAPI()

app.mount("/static", StaticFiles(directory="../ui/build/static", check_dir=False), name="static")
DB_EXT_PATH = "movies-extended.db"

def get_ext_db():
    conn = sqlite3.connect(DB_EXT_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def serve_react_app():
   return FileResponse("../ui/build/index.html")

@app.get('/movies')
def get_movies():  # put application's code here
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    movies = cursor.execute('SELECT * FROM movies')

    output = []
    for movie in movies:
        movie = {
            'id': movie[0],
            'title': movie[1],
            'year': movie[2],
            'actors': movie[3].split(", ") if movie[3] else []}
        output.append(movie)
    return output

@app.get('/movies/{movie_id}')
def get_single_movie(movie_id:int):  # put application's code here
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    movie = cursor.execute(f"SELECT * FROM movies WHERE id={movie_id}").fetchone()
    if movie is None:
        return {'message': "Movie not found"}
    return {'title': movie[1], 'year': movie[2], 'actors': movie[3]}

@app.post("/movies")
def add_movie(movie: Movie):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    actors_str = ", ".join(movie.actors)
    cursor.execute(
        "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
        (movie.title, movie.year, actors_str)
    )
    db.commit()
    return {"message": f"Movie with id = {cursor.lastrowid} added successfully",
            "id": cursor.lastrowid}
    # movie = models.Movie.create(**movie.dict())
    # return movie

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()

    actors_str = ", ".join(movie.actors)

    cursor.execute(
        "UPDATE movies SET title = ?, year = ?, actors = ? WHERE id = ?",
        (movie.title, movie.year, actors_str, movie_id)
    )
    db.commit()

    if cursor.rowcount == 0:
        return {"message": f"Movie with id = {movie_id} not found"}

    return {"message": "Movie updated"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id:int):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    db.commit()
    if cursor.rowcount == 0:
        return {"message": f"Movie with id = {movie_id} not found"}
    return {"message": f"Movie with id = {movie_id} deleted successfully"}

@app.delete("/movies")
def delete_movies(movie_id:int):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM movies")
    db.commit()
    return {"message": f"Deleted {cursor.rowcount} movies"}

@app.get("/actors")
def get_actors():
    conn = get_ext_db()
    rows = conn.execute("SELECT * FROM actor").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/actors/{actor_id}")
def get_actor(actor_id: int):
    conn = get_ext_db()
    row = conn.execute("SELECT * FROM actor WHERE id = ?", (actor_id,)).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Actor not found")

    return dict(row)


@app.post("/actors")
def add_actor(params: dict[str, Any]):
    conn = get_ext_db()
    cur = conn.execute(
        "INSERT INTO actor (name, surname) VALUES (?, ?)",
        (params.get("name"), params.get("surname"))
    )
    conn.commit()
    actor_id = cur.lastrowid
    conn.close()

    return {"message": "Actor added", "id": actor_id}


@app.put("/actors/{actor_id}")
def update_actor(actor_id: int, params: dict[str, Any]):
    conn = get_ext_db()
    cur = conn.execute(
        "UPDATE actor SET name = ?, surname = ? WHERE id = ?",
        (params.get("name"), params.get("surname"), actor_id)
    )
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Actor not found")

    return {"message": "Actor updated"}


@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    conn = get_ext_db()
    cur = conn.execute("DELETE FROM actor WHERE id = ?", (actor_id,))
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Actor not found")

    return {"message": "Actor deleted"}


# if __name__ == '__main__':
#     app.run()
