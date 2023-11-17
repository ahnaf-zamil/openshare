# flake8: noqa

from dotenv import load_dotenv

load_dotenv()

from src.app import create_app
from src.model import *

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
