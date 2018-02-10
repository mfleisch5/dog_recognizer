from flask import Flask

application = Flask(__name__)


@application.route('/')
def index():
    return 'Hello dogs'


application.debug = True

if __name__ == '__main__':
    application.run()

