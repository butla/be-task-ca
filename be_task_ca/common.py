from fastapi import Request

APP_PORT = 8000


def get_db(request: Request):
    return request.state.db
