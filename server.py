"""Create the server."""

import socket
import pickle
import settings as settings
from game import Game
from _thread import *


# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((settings.server, settings.port))
except socket.error as e:
    str(e)

s.listen()  # get connections
print("Waiting for a connection, Server Started")

games: dict[int, Game] = {}  # store games
id_count: int = 0  # store user count


# thread function
def threaded(connection, player_no: int, id_count: int, game_id: int) -> None:
    """
    Set up game data connection.

    Parameters
    ----------
        connection:
        player_no: which player user is
        id_count: the number of users there are
        game_id: the number of games per 2 users

    """
    connection.send(str.encode(str(player_no)))

    reply: None | Game = None
    while True:
        try:
            data = connection.recv(2048 * 2).decode()  # receive data

            # check if game still exists
            if game_id in games:
                game = games[game_id]

                if not data:
                    break

                # check data received
                else:
                    # reset game once game has finished
                    if data == "reset":
                        game.reset()
                    # send move data
                    elif data != "get":
                        game.play(player_no, data)

                    reply = game
                    # send response
                    connection.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

        # connection has been lost, so disconnect both
        print("Lost connection")
        try:
            del games[game_id]  # remove disconnected game
            print("Closing game", game_id)
        except KeyError:
            pass
        id_count -= 1
        connection.close()


while True:
    # establish client connection
    connection, addr = s.accept()
    print("Connection to:", addr)

    id_count += 1  # store user count
    player = 0  # establish which 'player' user is (i.e. 0 or 1)

    # create games for every 2 players
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        # create a new game
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        # send 2nd player to the game
        games[game_id].ready = True
        player = 1

    # start a new thread connection
    start_new_thread(threaded, (connection, player, id_count, game_id))
