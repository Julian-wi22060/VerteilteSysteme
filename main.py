from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWord(Resource):
    def get(self):
        return {"HelloWorld"}
    
api.add_resource(HelloWord, "/helloworld")

if __name__ == "__name__":
    app.run(debug=True)