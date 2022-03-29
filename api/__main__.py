'''
File for starting the flask app via python module execution
'''

from .app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
