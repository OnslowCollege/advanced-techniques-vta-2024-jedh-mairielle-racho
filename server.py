"""Create the server."""

import socket
from _thread import *
import pickle

server = "10.203.11.10"
port = 555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
id_count = 0


# thread function
def threaded(connection, player, game_id):
    """Set up game data connection."""
    connection.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = connection.recv(2048 * 2).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    # reset game once game has finished
                    if data == "reset":
                        pass
                    # get the game if users wish to start a game
                    elif data != "get":
                        pass

                    # send game data
                    connection.sendall(pickle.dumps(game))

            else:
                break
        except:
            break

        # connection has been lost, so disconnect both
        print("Lost connection")
        try:
            del games[game_id]
            print("Closing game", game_id)
        except:
            pass
        id_count -= 1
        connection.close()


while True:
    # establish client connection
    connection, addr = s.accept()
    print("Connection to:", addr)

    id_count += 1  # store user count
    player = 0
    game_id = (id_count - 1) // 2  # create games for every 2 players
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        player = 1

    # start a new thread connection
    start_new_thread(threaded, (connection, player, game_id))
