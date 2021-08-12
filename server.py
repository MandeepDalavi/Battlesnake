import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Mandeep Dalavi",  # TODO: Your Battlesnake Username
            "color": "#CF9FFF",  # TODO: Personalize
            "head": "beluga",  # TODO: Personalize
            "tail": "curled",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        body = data["you"]["body"]

        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        safe_moves = self.getSafeMoves(possible_moves, body, data["board"])

        if safe_moves:
          move = random.choice(safe_moves)
          return {"move" : move}

        return {"move" : 'up'}

    def getNext(self, currentHead, nextMove):
        futureHead = currentHead.copy()
        if nextMove == 'left':
            futureHead['x'] = currentHead['x'] - 1
        if nextMove == 'right':
            futureHead['x'] = currentHead['x'] + 1
        if nextMove == 'up':
            futureHead['y'] = currentHead['y'] + 1
        if nextMove == 'down':
            futureHead['y'] = currentHead['y'] - 1
        return futureHead
    
    def getSafeMoves(self, possible_moves, body, board):
        safe_moves = []

        for guess in possible_moves:
            # check if we make this move, will the decisions
            guessCoord = self.getNext(body[0], guess)
            if self.avoidWalls(guessCoord, board["width"], board["height"]) and self.avoidSnakes(guessCoord, board["snakes"]):
                safe_moves.append(guess)
            elif len(body)>1 and guessCoord == body[-1] and guess not in body[:-1]:
                safe_moves.append(guess)
        return safe_moves

    def avoidWalls(self, futureHead, width, height):
        result = True
        x = int(futureHead['x'])
        y = int(futureHead['y'])

        if x < 0 or y < 0 or x >= width or y >= height:
            result = False

        return result

    def avoidSnakes(self, futureHead, snakeBodies):
        for snake in snakeBodies:
            if futureHead in snake["body"][:-1]:
                return False
            return True

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
