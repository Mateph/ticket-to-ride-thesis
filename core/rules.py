from core.models import ClaimRoute, GameMap, GameState, PlayerState, Route

STARTING_TRAINS = 5
MIN_PLAYERS = 2

RULE_POINTS = {1:1, 2:2, 3:4, 4:7, 5:10, 6:15}

Action = ClaimRoute

class RuleError(Exception):
    pass


#region finders

def find_route(game_map: GameMap, route_id: str) -> Route | None:
    return next((route for route in game_map.routes if route.id == route_id),None)

def find_player_index(state: GameState, player_name: str)-> int | None:
    return next((index for index, player in enumerate(state.players) if player.name == player_name),None)

#endregion

#region actions

def new_game(game_map: GameMap, player_names: list[str]) -> GameState:   
    if len(player_names) < MIN_PLAYERS:
        raise RuleError(f"At least {MIN_PLAYERS} players are needed for game start") 
    
    if len(set(player_names)) != len(player_names):
        raise RuleError("All player names must be unique")
    players = [
        PlayerState (name = name, trains_left=STARTING_TRAINS,score=0)
        for name in player_names
    ]
    route_owners = {route.id : None for route in game_map.routes}
    return GameState(players=players, route_owners=route_owners, current_player_index=0)

def apply_action(state:GameState, player_name:str, action:Action, game_map:GameMap) -> GameState:
    match action:
        case ClaimRoute():
            return _claim_route(state,player_name,action,game_map)
            
        case _:
            raise RuleError("Unknown action")

#endregion

#region applicable_actions

def _claim_route(state:GameState, player_name:str, action: Action, game_map:GameMap) -> GameState:
    player_index = find_player_index(state, player_name)

    if (player_index == None):
        raise RuleError("Unknown player index")
    if (player_index != state.current_player_index):
        raise RuleError("It is not the player's turn")

    route = find_route(game_map, action.route_id)
    if (route is None): 
        raise RuleError("Non existant route")
    if (state.route_owners[route.id] is not None):
        raise RuleError("Route is already claimed")
    
    if (state.players[player_index].trains_left < route.length):
        raise RuleError("Not enough trains for this action")
    
    new_state =state.model_copy(deep=True)
    new_state.route_owners[route.id] = player_name
    new_state.players[player_index].trains_left -= route.length
    new_state.players[player_index].score += RULE_POINTS[route.length]
    new_state.current_player_index = (state.current_player_index + 1)% len(new_state.players)

    return new_state

#endregion
    