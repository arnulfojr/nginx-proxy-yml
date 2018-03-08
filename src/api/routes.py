from aiohttp.web import Response


async def hello_world(request):
    return Response(text="Hello World")


async def ping(request):
    return Response(body="Guacamole!")


async def register_service(request):
    """POST registers a service"""
    return Response(status=201)


async def deregister_service(request):
    return Response(status=203)


async def refresh(request):
    """PUT refreshes the service"""
    service_id = request.match_info['id']
    return Response(status=200)


def register_routes(app):
    app.router.add_get('/hello', hello_world)
    app.router.add_get('/ping', ping)
    app.router.add_post('/services', register_service)
    app.router.add_put('/services/{id}', refresh)
    app.router.add_delete('/services/{id}', deregister_service)
