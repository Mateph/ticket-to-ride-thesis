import pytest

from core.models import ClaimRoute, GameMap
from core.rules import (
    MIN_PLAYERS,
    STARTING_TRAINS,
    RuleError,
    apply_action,
    new_game,
)


def claim_route(route_id: str) -> ClaimRoute:
    return ClaimRoute(action="claim", route_id=route_id)


def get_route_index_by_id(route_id: str, map: GameMap) -> int:
    return next(i for i, route in enumerate(map.routes) if route.id == route_id)


class TestNewGame:
    def test_short_list(self, game_map):
        short_list = [""]

        with pytest.raises(RuleError) as excinfo:
            new_game(game_map=game_map, player_names=short_list)
        assert (
            excinfo.value.args[0]
            == f"At least {MIN_PLAYERS} players are needed for game start"
        )

    def test_non_unique_list(self, game_map):
        non_unique_list = ["apple", "apple"]

        with pytest.raises(RuleError, match="player names must be unique"):
            new_game(game_map=game_map, player_names=non_unique_list)

    def test_new_game(self, game_map, state):
        assert state.players[0].name == "apple"
        assert state.players[0].trains_left == STARTING_TRAINS
        assert state.players[0].score == 0

        assert state.players[1].name == "pear"
        assert state.players[1].trains_left == STARTING_TRAINS
        assert state.players[1].score == 0

        empty_route_dict = {route.id: None for route in game_map.routes}
        assert empty_route_dict == state.route_owners
        assert state.current_player_index == 0


class TestClaim:
    def test_claim_success(self, game_map, state):
        test_route = game_map.routes[get_route_index_by_id("bud-vie-1", game_map)]
        testable_state = apply_action(
            state=state,
            player_name="apple",
            action=claim_route("bud-vie-1"),
            game_map=game_map,
        )

        assert (
            testable_state.players[0].trains_left == STARTING_TRAINS - test_route.length
        )
        assert testable_state.players[0].score == 2
        assert testable_state.route_owners[test_route.id] == "apple"
        assert testable_state.current_player_index == 1

    def test_double_claim(self, game_map, state):
        testable_state = apply_action(
            state=state,
            player_name="apple",
            action=claim_route("bud-vie-1"),
            game_map=game_map,
        )

        with pytest.raises(RuleError, match="already claimed"):
            apply_action(
                state=testable_state,
                player_name="pear",
                action=claim_route("bud-vie-1"),
                game_map=game_map,
            )

    def test_not_players_turn(self, game_map, state):
        test_state = state.model_copy(deep=True)
        test_state.current_player_index = 1

        with pytest.raises(RuleError, match="not the player's turn"):
            apply_action(
                state=test_state,
                player_name="apple",
                action=claim_route("bud-vie-1"),
                game_map=game_map,
            )

    def test_unknown_player(self, game_map, state):
        with pytest.raises(RuleError, match="Unknown player index"):
            apply_action(
                state=state,
                player_name="banana",
                action=claim_route("bud-vie-1"),
                game_map=game_map,
            )

        state_without_player = state.model_copy(deep=True)
        test_name_id = 0
        for player in state_without_player.players:
            player.name = f"P{test_name_id}"

        with pytest.raises(RuleError, match="Unknown player index"):
            apply_action(
                state=state_without_player,
                player_name="apple",
                action=claim_route("bud-vie-1"),
                game_map=game_map,
            )

    def test_not_enough_trains(self, game_map, state):
        test_state = state.model_copy(deep=True)
        test_state.players[0].trains_left = 1
        with pytest.raises(RuleError, match="Not enough trains"):
            apply_action(
                state=test_state,
                player_name="apple",
                action=claim_route("bud-vie-1"),
                game_map=game_map,
            )

    def test_non_existant_route(self, game_map, state):
        test_map = game_map.model_copy(deep=True)
        test_map.routes[get_route_index_by_id("bud-vie-1", test_map)].id = (
            "Seattle-Georgia"
        )

        with pytest.raises(RuleError, match="Non existant route"):
            apply_action(
                state=state,
                player_name="apple",
                action=claim_route("bud-vie-1"),
                game_map=test_map,
            )

        with pytest.raises(RuleError, match="Non existant route"):
            apply_action(
                state=state,
                player_name="apple",
                action=claim_route("Non-existant-route"),
                game_map=test_map,
            )

    def test_unknown_action(self, game_map, state):
        test_action_1 = None
        with pytest.raises(RuleError, match="Unknown action"):
            apply_action(
                state=state,
                player_name="apple",
                action=test_action_1,
                game_map=game_map,
            )

        test_action_2 = ("some", [(1, "object")])
        with pytest.raises(RuleError, match="Unknown action"):
            apply_action(
                state=state,
                player_name="apple",
                action=test_action_2,
                game_map=game_map,
            )

    def test_no_change_to_base_state(self, game_map, state):
        state_save = state.model_dump()
        testable_state = apply_action(
            state=state,
            player_name="apple",
            action=claim_route("bud-vie-1"),
            game_map=game_map,
        )
        assert testable_state is not state_save
        assert testable_state != state_save

        state_save = state.model_dump()
        with pytest.raises(RuleError):
            testable_state = apply_action(
                state=testable_state,
                player_name="apple",
                action=claim_route("bud-vie-1"),
                game_map=game_map,
            )

        assert testable_state is not state_save
        assert testable_state != state_save

    def test_current_player_index_resets(self, game_map, state):
        counter = 0
        for player in state.players:
            assert state.current_player_index == counter
            new_state = apply_action(
                state=state,
                player_name=player.name,
                action=claim_route(game_map.routes[counter].id),
                game_map=game_map,
            )
            state = new_state
            counter = counter + 1

        assert state.current_player_index == 0
