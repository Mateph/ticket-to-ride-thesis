from typing import Literal, Self

from pydantic import BaseModel, StrictInt, model_validator

ALLOWED_COLORS = {"red", "white", "green", "gray", "black", "yellow", "purple", "pink"}
ALLOWED_ROUTE_TYPES = {"normal", "tunnel", "ferry"}

MAX_ROUTE_LENGTH = 7
ALLOWED_ROUTE_LENGTHS = {i for i in range(1, MAX_ROUTE_LENGTH + 1)}
# region map


class City(BaseModel):
    id: str
    name: str
    x: StrictInt
    y: StrictInt


class Route(BaseModel):
    id: str
    a: str
    b: str
    length: StrictInt
    color: str
    type: str

    @model_validator(mode="after")
    def only_allowed_color_types_check(self) -> Self:
        if self.color not in ALLOWED_COLORS:
            raise ValueError(f"Not allowed color: {self.color}")
        return self

    @model_validator(mode="after")
    def only_allowed_route_types_check(self) -> Self:
        if self.type not in ALLOWED_ROUTE_TYPES:
            raise ValueError(f"Not allowed route type: {self.type}")
        return self

    @model_validator(mode="after")
    def only_allowed_route_length_check(self) -> Self:
        if self.length not in ALLOWED_ROUTE_LENGTHS:
            raise ValueError(f"Not allowed route length: {self.length}")
        return self

    @model_validator(mode="after")
    def different_start_end_point_check(self) -> Self:
        if self.a == self.b:
            raise ValueError(
                f"One route can't have the same start and end point: {self.a}"
            )
        return self


class GameMap(BaseModel):
    cities: list[City]
    routes: list[Route]

    @model_validator(mode="after")
    def no_routes_with_unknown_city_check(self) -> Self:
        route_endpoints = {r.a for r in self.routes} | {r.b for r in self.routes}
        city_ids = {c.id for c in self.cities}
        unknown_cities = route_endpoints - city_ids
        if unknown_cities:
            raise ValueError(f"Unknown cities found: {unknown_cities}")
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

    @model_validator(mode="after")
    def unique_route_ids_check(self) -> Self:
        for type, items in (("city", self.cities), ("route", self.routes)):
            ids = [item.id for item in items]
            duplicates = {i for i in ids if ids.count(i) > 1}
            if duplicates:
                raise ValueError(f"Duplicate {type} ids: {duplicates}")
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
