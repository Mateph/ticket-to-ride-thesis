from pydantic import BaseModel,StrictInt, model_validator
from typing import Self,Literal

#region map

#Todo: Make more validations
class City(BaseModel):
    id: str
    name: str
    x: StrictInt
    y: StrictInt

#Todo: Make more validations
class Route(BaseModel):
    id: str
    a: str
    b: str
    length: StrictInt
    color: str
    type: str

#Todo: Make more validations
class GameMap(BaseModel):
    cities: list[City]
    routes: list[Route]

    @model_validator(mode='after') 
    def min_one_route_for_every_city_check(self)->Self:
        used = {r.a for r in self.routes} | {r.b for r in self.routes}
        missing = [c.id for c in self.cities if c.id not in used]
        if missing:
            raise ValueError(f"Cities without any route: {missing}")
        return self
        
#endregion

#region state

class PlayerState(BaseModel):
    name: str
    trains_left: StrictInt
    score: StrictInt

class GameState(BaseModel):
    players: list[PlayerState]
    route_owners: dict[str,str | None]
    current_player: int

#endregion

#region actions

class ClaimRoute (BaseModel):
    action: Literal["claim"]
    route_id: str


#endregion





