# flake8: noqa

from dotenv import load_dotenv

load_dotenv()

from src.app import create_app
from src.model import *
from flask_migrate import migrate, upgrade

import argparse

parser = argparse.ArgumentParser(prog="OpenShare", description="OpenShare API")
parser.add_argument("command")

app = create_app()

if __name__ == "__main__":
    args = parser.parse_args()
    match args.command:
        case "run":
            app.run(port=5000, debug=True)
        case "upgrade":
            with app.app_context():
                upgrade()
        case _:
            print(f"Invalid command {args.command}")
