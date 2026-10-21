import pytest

from core.models import ClaimRoute
from core.rules import (
            MIN_PLAYERS,
            RULE_POINTS,
            STARTING_TRAINS,
            RuleError,
            apply_action,
            new_game,
)


def claim_route(route_id:str):
            return ClaimRoute(action="claim",route_id=route_id)

class TestNewGame:
    

    def test_short_list(self,game_map):
        short_list = [""]

        with pytest.raises(RuleError) as excinfo:
            new_game(game_map=game_map, player_names=short_list)
        assert excinfo.value.args[0] == f"At least {MIN_PLAYERS} players are needed for game start"

    def test_non_unique_list(self,game_map):
        non_unique_list = ["apple","apple"]

        with pytest.raises(RuleError) as excinfo:
                new_game(game_map=game_map, player_names=non_unique_list)
        assert excinfo.value.args[0] == "All player names must be unique"

    def test_new_game(self,game_map):
        passing_list = ["apple","pear"]

        state = new_game(game_map=game_map, player_names=passing_list)


        assert state.players[0].name == "apple"
        assert state.players[0].trains_left == STARTING_TRAINS
        assert state.players[0].score == 0

        assert state.players[1].name == "pear"
        assert state.players[1].trains_left == STARTING_TRAINS
        assert state.players[1].score == 0


        empty_route_dict = {route.id : None for route in game_map.routes}        
        assert empty_route_dict == state.route_owners
        assert state.current_player_index == 0

class TestClaim:
    def test_claim_success(self,game_map,state):
        test_route = next(route for route in game_map.routes if route.id == "bud-vie-1" )
        testable_state = apply_action(state=state,player_name="apple",action=claim_route("bud-vie-1"),game_map=game_map)

        assert testable_state.players[0].trains_left == STARTING_TRAINS-test_route.length
        assert testable_state.players[0].score == RULE_POINTS[test_route.length]
        assert testable_state.route_owners[test_route.id] == "apple"
        assert testable_state.current_player_index == 1

    def test_double_claim(self,game_map,state):
        testable_state = apply_action(state=state,player_name="apple",action=claim_route("bud-vie-1"),game_map=game_map)

        with pytest.raises(RuleError, match="already claimed"):
            apply_action(state=testable_state,player_name="pear",action=claim_route("bud-vie-1"),game_map=game_map)

    def test_not_players_turn(self,game_map,state):
        test_state = state.model_copy(deep=True)
        test_state.current_player_index = 1
        
        with pytest.raises(RuleError, match="not the player's turn"):
            apply_action(state=test_state,player_name="apple",action=claim_route("bud-vie-1"),game_map=game_map)

    def test_unknown_player(self,game_map, state):
        with pytest.raises(RuleError, match= "Unknown player index"):
            apply_action(state=state,player_name="banana",action=claim_route("bud-vie-1"),game_map=game_map)

        state_without_player = state.model_copy(deep=True)
        test_name_id = 0
        for player in state_without_player.players:
            player.name = f"P{test_name_id}"
        
        with pytest.raises(RuleError, match= "Unknown player index"):
            apply_action(state=state_without_player,player_name="apple",action=claim_route("bud-vie-1"),game_map=game_map)

    def test_not_enough_trains(self,game_map,state):
        test_state = state.model_copy(deep=True)
        test_state.players[0].trains_left = 0
        with pytest.raises(RuleError, match="Not enough trains"):
            apply_action(state=test_state,player_name="apple",action=claim_route("bud-vie-1"), game_map=game_map)