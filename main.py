from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.loader import load_map
from core.models import ClaimRoute, GameMap, GameState
from core.rules import RuleError, apply_action, new_game


class ClaimRequest(BaseModel):
    player_name: str
    route_id:str


app = FastAPI()
game_map = load_map()

PLAYERS = ["alma", "körte"]

store = {"game_state" : new_game(game_map,PLAYERS)}

origins = ["http://localhost:5173"]

app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get("/api/map")
def get_map() -> GameMap:
    return game_map


@app.get("/api/state")
def get_state() -> GameState:
    return store["game_state"]

@app.post("/api/claim")
def post_claim(req:ClaimRequest) -> GameState:

    try:
        new_game_state = apply_action(store["game_state"],req.player_name,ClaimRoute(action="claim",route_id=req.route_id),game_map)
    except RuleError as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        store["game_state"] = new_game_state
    return new_game_state
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


    





