'''Module documentation'''

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    '''Function documentation'''
    return 'Hello World!'

if __name__ == "__main__":
    app.run()
