from sqlalchemy.ext.asyncio import async_sessionmaker


def create_session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False)
