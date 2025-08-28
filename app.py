from flask import Flask

def creat_app():
    app = Flask(__name__)
    from rountes import registerRoutes
    registerRoutes(app)

    return app