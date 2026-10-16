from fastapi import FastAPI

from core.loader import load_map

app = FastAPI()
game_map = load_map()

@app.get("/api/map")
def get_map():
    return game_map


