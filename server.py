"""Listen for connection requests."""
# MUST RUN SERVER BEFORE PLAYING BLACKJACK

import socket
import pickle
import settings as s
from game import Game
from _thread import *

# create a listening socket
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connection.bind((s.SERVER, s.PORT))  # bind server to IP
except socket.error as er_m:
    # error occurrence with binding to IP
    print(er_m)

connection.listen(2)
print("Server started! Connected blackjack now available!\n")

# store variables
games: dict[int, Game] = {}  # allows multiple games at once
id_count: int = 0  # how many users are playing


# run multiple programs using threading
def threaded(connection, player_no: int, game_id: int) -> None:
    """
    Create/connect to a branch game.

    Parameters
    ----------
        connection: socket connection link for user
        player_no: the numbered player the user is
        id_count: the number of playing users
        game_id: the specific game of the user to connect to

    """
    global id_count
    connection.send(str.encode(str(player_no)))

    # check thread conditions
    while True:
        try:
            data = connection.recv(2048 * 2).decode()  # receive data

            # check if game exists
            if game_id in games:  # connect two clients to a game
                game = games[game_id]

                # check data received
                if not data:
                    break
                else:
                    if data == "reset":
                        # reset game once finished
                        game.reset()

                    elif data == "hit":
                        # player hits
                        game.hit(player_no)

                    elif data == "stand":
                        game.stand(player_no)

                    elif data == "next round":
                        # send the player's turn
                        game.next_round()

                    elif data == "finished":
                        print("Game finished")
                        break

                    # send response to server socket
                    connection.sendall(pickle.dumps(game))

            else:  # game doesn't exit (i.e. a player disconnects)
                # connection has been lost, so disconnect both
                print("Lost connection")
                break
        except socket.error:  # error in receiving data occurred
            break

    # delete game
    try:
        del games[game_id]
        print("Closing game", game_id)
    except KeyError:  # when game has already been deleted
        pass

    id_count -= 1
    connection.close()


while True:
    # establish connection
    sock, address = connection.accept()
    print("Connection to:", address)

    id_count += 1
    print(id_count)
    player = 0  # i.e. player 1

    # create games for every 2 players
    game_id = (id_count - 1) // 2
    # create a new game if user is player 1
    if id_count % 2 == 1:
        games[game_id] = Game()
        print(f"Creating a new game {game_id}...")

    # if user is player 2, send to a game
    else:
        print(f"Connecting to game {game_id}...\n")
        games[game_id].ready = True
        player = 1  # i.e. player 2

    # start a new thread
    start_new_thread(threaded, (sock, player, game_id))
