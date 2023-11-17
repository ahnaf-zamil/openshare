import os


class AppConfig:
    DATABASE_URI = os.environ["DATABASE_URI"]
    SECRET_KEY = os.environ["SECRET_KEY"]

    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
