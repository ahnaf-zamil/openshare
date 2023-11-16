# flake8: noqa
from .src.app import create_app
from .src.model import *

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
