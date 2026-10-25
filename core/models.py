from typing import Literal, Self

from pydantic import BaseModel, StrictInt, model_validator

# region map


# Todo: Make more validations
class City(BaseModel):
    id: str
    name: str
    x: StrictInt
    y: StrictInt


# Todo: Make more validations
class Route(BaseModel):
    id: str
    a: str
    b: str
    length: StrictInt
    color: str
    type: str


# Todo: Make more validations
class GameMap(BaseModel):
    cities: list[City]
    routes: list[Route]

    @model_validator(mode="after")
    def no_routes_with_unknown_city_check(self) -> Self:
        route_endpoints = {r.a for r in self.routes} | {r.b for r in self.routes}
        city_ids = {c.id for c in self.cities}
        unknown_cities = route_endpoints - city_ids
        if unknown_cities:
            raise ValueError(f"Unkown cities found: {unknown_cities}")
        return self

    @model_validator(mode="after")
    def min_one_route_for_every_city_check(self) -> Self:
        route_endpoints = {r.a for r in self.routes} | {r.b for r in self.routes}
        city_ids = {c.id for c in self.cities}
        missing_cities = city_ids - route_endpoints
        if missing_cities:
            raise ValueError(f"Cities without any route: {missing_cities}")
        return self

    @model_validator(mode="after")
    def multiple_cities_at_one_coordinate(self) -> Self:
        city_coordinates = [(c.x, c.y) for c in self.cities]
        duplicates = [i for i in set(city_coordinates) if city_coordinates.count(i) > 1]
        if duplicates != []:
            raise ValueError(f"More cities have the same coordinates: {duplicates}")
        return self


# endregion

# region state


class PlayerState(BaseModel):
    name: str
    trains_left: StrictInt
    score: StrictInt


class GameState(BaseModel):
    players: list[PlayerState]
    route_owners: dict[str, str | None]  # Route,Owner
    current_player_index: int


# endregion

# region actions


class ClaimRoute(BaseModel):
    action: Literal["claim"]
    route_id: str


# endregion
