from pathlib import Path

import pytest

from core.loader import load_map
from core.models import ClaimRoute
from core.rules import RULE_POINTS, STARTING_TRAINS, apply_action, new_game


class RuleError(Exception):
    pass

class TestNewGame:
    TEST_PATH = Path(__file__).parent.parent/"core" / "data" / "map_testmap1.json"
    game_map = load_map(TEST_PATH)

    def test_short_list(self):
        short_list = [""]

        with pytest.raises(RuleError):
            state = new_game(game_map=self.game_map, player_names=short_list)

    def test_non_unique_list(self):
        non_unique_list = ["apple","apple"]

        with pytest.raises(RuleError):
                state = new_game(game_map=self.game_map, player_names=non_unique_list)

    def test_new_game(self):
        passing_list = ["apple","pear"]

        state = new_game(game_map=self.game_map, player_names=passing_list)


        assert state.players[0].name == "apple"
        assert state.players[0].trains_left == STARTING_TRAINS
        assert state.players[0].score == 0

        assert state.players[1].name == "pear"
        assert state.players[1].trains_left == STARTING_TRAINS
        assert state.players[1].score == 0
        
        #assert state.route_owners[0] == None
        assert state.current_player_index == 0






class TestClaim:
    TEST_PATH = Path(__file__).parent.parent/"core" / "data" / "map_testmap1.json"
    game_map = load_map(TEST_PATH)

    
    player_list = ["apple", "pear"]

    def test_claim_success(self):
        claim_route_0 = ClaimRoute(action="claim",route_id=self.game_map.routes[0].id)
        state = new_game(game_map=self.game_map, player_names=self.player_list)

        testable_state = apply_action(state=state,player_name="apple",action=claim_route_0,game_map=self.game_map)

        test_route = self.game_map.routes[0]

        assert testable_state.players[0].trains_left == STARTING_TRAINS-test_route.length
        assert testable_state.players[0].score == RULE_POINTS[test_route.length]
        assert testable_state.route_owners[test_route.id] == "apple"
        assert testable_state.current_player_index == 1
         

    
    
     
    
    




