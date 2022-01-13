from models import Game, User


CREATE_GAME = "INSERT INTO game (name, category, console) VALUES (%s, %s, %s)"
UPDATE_GAME = "UPDATE game SET name = %s, category = %s, console = %s WHERE pk = %s"
SELECT_GAME_BY_PK = "SELECT pk, name, category, console FROM game WHERE pk = %s"
SELECT_ALL_GAMES = "SELECT pk, name, category, console FROM game"
DELETE_GAME = "DELETE FROM game WHERE pk = %s"

SELECT_USER_BY_USERNAME = "SELECT pk, username, password FROM user WHERE username = %s"


class GameDAO:
    def __init__(self, db) -> None:
        self.__db = db

    def save(self, game) -> Game:
        cursor = self.__db.connection.cursor()

        if game.pk:
            cursor.execute(UPDATE_GAME, (game.name, game.category, game.console, game.pk))
        else:
            cursor.execute(CREATE_GAME, (game.name, game.category, game.console))
            game.pk = cursor.lastrowid

        self.__db.connection.commit()
        return game

    def list(self):
        cursor = self.__db.connection.cursor()

        cursor.execute(SELECT_ALL_GAMES)
        games = translate_games(cursor.fetchall())

        return games

    def query_by_pk(self, pk) -> Game:
        cursor = self.__db.connection.cursor()

        cursor.execute(SELECT_GAME_BY_PK, (pk,))
        data = cursor.fetchone()

        return Game(data[1], data[2], data[3], data[0])

    def delete(self, pk) -> None:
        self.__db.connection.cursor().execute(DELETE_GAME, (pk,))
        self.__db.connection.commit()


class UserDAO:
    def __init__(self, db) -> None:
        self.__db = db

    def query_by_username(self, username) -> User:
        cursor = self.__db.connection.cursor()
        cursor.execute(SELECT_USER_BY_USERNAME, (username,))
        data = cursor.fetchone()
        user = translate_user(data) if data else None
        return user


def translate_games(games):
    def create_game_with_tuple(tuple):
        return Game(tuple[1], tuple[2], tuple[3], tuple[0])
    return list(map(create_game_with_tuple, games))

def translate_user(tuple):
    return User(tuple[1], tuple[2], tuple[0])
