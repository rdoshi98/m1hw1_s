from uuid import uuid4
from typing import List, Tuple, Dict, Union
from blackjack.blackjack import Blackjack
import asyncio


class AsyncBlackjackGameDB(object):
    def __init__(self):
        self._current_games: Dict[str, Blackjack] = {}
        self._termination_passwords: Dict[str, str] = {}
        self._QUERY_TIME: float = 0.05

    async def add_game(self, num_players: int, num_decks: int = 2) -> Tuple[str, str]:
        """
        Asks the database to create a new game.

        :param num_players: number of players
        :param num_decks: number of decks to use, default 2
        :return: the UUID (universally-unique ID) of the game
        """
        await asyncio.sleep(self._QUERY_TIME)  # simulate query time
        game_uuid = str(uuid4())
        game_term_password = str(uuid4())
        self._current_games[game_uuid] = Blackjack(num_decks, num_players)
        self._termination_passwords[game_uuid] = game_term_password
        return game_uuid, game_term_password

    async def list_games(self) -> List[Tuple[str, int]]:
        """
        Asks the database for a list of all active games.

        :return: list of (game_id, number of players in game)
        """
        await asyncio.sleep(self._QUERY_TIME)  # simulate query time
        return [(game_id, game.num_players) for game_id, game in self._current_games.items()]

    async def get_game(self, game_id: str) -> Union[Blackjack, None]:
        """
        Asks the database for a pointer to a specific game.

        :param game_id: the UUID of the specific game
        :return: None if the game was not found, otherwise pointer to the Blackjack object
        """
        await asyncio.sleep(self._QUERY_TIME)  # simulate query time
        return self._current_games.get(game_id, None)

    async def del_game(self, game_id: str, term_pass: str) -> bool:
        """
        Asks the database to terminate a specific game.

        :param game_id: the UUID of the specific game
        :param term_pass: the termination password for the game
        :return: False or exception if not found, True if success
        """
        try:
            await asyncio.sleep(self._QUERY_TIME)  # simulate query time
            if self._termination_passwords[game_id] == term_pass:
                del self._current_games[game_id]
                return True
            else:
                return False
        except KeyError:
            return False
