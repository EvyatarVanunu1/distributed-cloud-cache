from flask_restful import Resource


class Heartbeat(Resource):

    def get(self):
        return "I'm Alive!", 200
