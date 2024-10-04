from ports.api.v1.contracts import Request


async def roster(
    request: Request,
    address: str
):
    query_provider = request.app.query_provider
    data, quantity = await query_provider.get_logs(address)
    return {
        'data': data,
        'meta': {
            'quantity': quantity
        }
    }


async def parse(
    request: Request,
):
    await request.app.logs_processor()
    return {
        'data': 'ok'
    }
