from pathlib import Path

import pytest

from core.loader import load_map
from core.models import ClaimRoute
from core.rules import (
    MIN_PLAYERS,
    RULE_POINTS,
    STARTING_TRAINS,
    RuleError,
    apply_action,
    new_game,
)


class TestNewGame:
    TEST_PATH = Path(__file__).parent.parent/"core" / "data" / "map_testmap1.json"
    game_map = load_map(TEST_PATH)

    def test_short_list(self):
        short_list = [""]

        with pytest.raises(RuleError) as excinfo:
            new_game(game_map=self.game_map, player_names=short_list)
        assert excinfo.value.args[0] == f"At least {MIN_PLAYERS} players are needed for game start"

    def test_non_unique_list(self):
        non_unique_list = ["apple","apple"]

        with pytest.raises(RuleError) as excinfo:
                new_game(game_map=self.game_map, player_names=non_unique_list)
        assert excinfo.value.args[0] == "All player names must be unique"

    def test_new_game(self):
        passing_list = ["apple","pear"]

        state = new_game(game_map=self.game_map, player_names=passing_list)


        assert state.players[0].name == "apple"
        assert state.players[0].trains_left == STARTING_TRAINS
        assert state.players[0].score == 0

        assert state.players[1].name == "pear"
        assert state.players[1].trains_left == STARTING_TRAINS
        assert state.players[1].score == 0


        empty_route_dict = {route.id : None for route in self.game_map.routes}        
        assert empty_route_dict == state.route_owners
        assert state.current_player_index == 0

class TestClaim:
    TEST_PATH = Path(__file__).parent.parent/"core" / "data" / "map_testmap1.json"
    game_map = load_map(TEST_PATH)
    player_list = ["apple", "pear"]  # noqa: RUF012

    def test_claim_success(self):
        claim_route_0 = ClaimRoute(action="claim",route_id=self.game_map.routes[0].id)
        state = new_game(game_map=self.game_map, player_names=self.player_list)

        testable_state = apply_action(state=state,player_name="apple",action=claim_route_0,game_map=self.game_map)

        test_route = self.game_map.routes[0]

        assert testable_state.players[0].trains_left == STARTING_TRAINS-test_route.length
        assert testable_state.players[0].score == RULE_POINTS[test_route.length]
        assert testable_state.route_owners[test_route.id] == "apple"
        assert testable_state.current_player_index == 1

    def test_double_claim(self):
        claim_route_0 = ClaimRoute(action="claim",route_id=self.game_map.routes[0].id)
        state = new_game(game_map=self.game_map, player_names=self.player_list)
        
        testable_state = apply_action(state=state,player_name="apple",action=claim_route_0,game_map=self.game_map)

        with pytest.raises(RuleError) as excinfo:
            apply_action(state=testable_state,player_name="pear",action=claim_route_0,game_map=self.game_map)
        assert excinfo.value.args[0] == "Route is already claimed"

    def test_not_players_turn(self):
        claim_route_0 = ClaimRoute(action="claim",route_id=self.game_map.routes[0].id)
        claim_route_1 = ClaimRoute(action="claim",route_id=self.game_map.routes[1].id)
        state = new_game(game_map=self.game_map, player_names=self.player_list)
        
        testable_state = apply_action(state=state,player_name="apple",action=claim_route_0,game_map=self.game_map)

        with pytest.raises(RuleError) as excinfo:
            apply_action(state=testable_state,player_name="apple",action=claim_route_1,game_map=self.game_map)
        assert excinfo.value.args[0] == "It is not the player's turn"

    def test_unknown_player_index(self):
        claim_route_0 = ClaimRoute(action="claim",route_id=self.game_map.routes[0].id)
        state_with_player = new_game(game_map=self.game_map, player_names=self.player_list)

        with pytest.raises(RuleError) as excinfo:
            apply_action(state=state_with_player,player_name="banana",action=claim_route_0,game_map=self.game_map)
        assert excinfo.value.args[0] == "Unknown player index"

        playerlist_without_certain_player = ["pear", "plum"]
        state_without_certain_player = new_game(game_map=self.game_map, player_names=playerlist_without_certain_player)
        with pytest.raises(RuleError) as excinfo:
            apply_action(state=state_without_certain_player,player_name="apple",action=claim_route_0,game_map=self.game_map)
        assert excinfo.value.args[0] == "Unknown player index"

    def test_not_enough_trains(self):
        state = new_game(game_map=self.game_map, player_names=self.player_list)

        def claimRoute(i:int):
            return ClaimRoute(action="claim",route_id=self.game_map.routes[i].id)


        for i in range (4):
            player = "apple" if i%2==0 else "pear"
            new_state = apply_action(state=state,player_name=player,action=claimRoute(i),game_map=self.game_map)
            state = new_state
            
        with pytest.raises(RuleError) as excinfo:
            apply_action(state=state,player_name="apple",action=claimRoute(4),game_map=self.game_map)
        assert excinfo.value.args[0] == "Not enough trains for this action"



                





         

    
         

    
    
     
    
    




