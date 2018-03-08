from aiohttp import web
from .routes import register_routes


app = web.Application()

register_routes(app)
