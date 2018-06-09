from aiopg.sa import create_engine

async def init_pg(app):
    engine = await create_engine(
        database="fof",
        user="postgres",
        host="localhost",
        port="5432"
    )
    app['db'] = engine

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
