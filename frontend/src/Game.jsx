import React, { useEffect, useState } from "react";
import api from "./api";

const RouteList = () => {
  const [gameMap, setGameMap] = useState(null);
  const [game, setGame] = useState(null);

  const [gameError, setError] = useState("");

  const fetchGameMap = async () => {
    try {
      const response = await api.get("/map");
      setGameMap(response.data);
    } catch (error) {
      console.error("Error fetching game map", error);
    }
  };

  const fetchGame = async () => {
    try {
      const response = await api.get("/state");
      setGame(response.data);
    } catch (error) {
      console.error("Error fetching game state", error);
    }
  };

  const claimRoute = async (playerName, routeID) => {
    try {
      await api.post("/claim", { player_name: playerName, route_id: routeID });
      fetchGame();

      setError("");
    } catch (error) {
      console.error("Error claiming route", error);
      setError(error.response?.data?.detail ?? "Unknown error");
    }
  };

  useEffect(() => {
    fetchGameMap();
    fetchGame();
  }, []);

  if (game === null || gameMap === null) {
    return (
      <div>
        <h2>Route list</h2>
        <p>Loading...</p>
      </div>
    );
  }

  const { routes } = gameMap;

  return (
    <div>
      <h2>Route list</h2>
      <p>{gameError}</p>
      <ul>
        {routes.map((route) => (
          <li key={route.id}>
            {route.id} Owned by: {game.route_owners[route.id]}
            <button
              type="button"
              onClick={() =>
                claimRoute(
                  game.players[game.current_player_index].name,
                  route.id,
                )
              }
            >
              Claim
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RouteList;
