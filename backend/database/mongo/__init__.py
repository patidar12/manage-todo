import re
from typing import Dict, List, Tuple
from typing import AsyncGenerator
from pymongo import ReadPreference
from asyncio.events import AbstractEventLoop
from motor.motor_asyncio import AsyncIOMotorClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

class _DbClient:
    DATABASES = {}
    mongo_url = r"^(mongodb:(?:\/{2})?)((\w+?):(\w+?)@|:?@?)(\S+?):(\d+)\/(\S+?)(\?replicaSet=(\S+?))?$"

    def __init__(
            self,
            databases: Dict[str, Dict[str, str]],
            loop: AbstractEventLoop,
            app_name: str
    ) -> None:
        regex = re.compile(self.mongo_url)
        for db_name, db_config in databases.items():
            print(db_name, db_config)
            assert isinstance(db_name, str), "Not a valid database name"
            connection = db_config.get("host")
            assert regex.search(connection), "Not a valid connection string."

            if self.DATABASES.get(db_name) is None:
                self.DATABASES[db_name] = AsyncIOMotorClient(
                    host = connection,
                    appname = app_name,
                    read_preference=db_config.get(
                        "read_preference", ReadPreference.SECONDARY_PREFERRED
                    ),
                    io_loop=loop
                ).get_default_database()


def connection(config: dict) -> None:
    # one time database connection setup
    # TODO: check else condition not passing loop will cause issue.
    if config.get("loop"):
        _DbClient(config.get("databases"), config.get("loop"), config.get("app_name"))
    else:
        _DbClient(config.get("databases"), config.get("app_name"))



def get_db_conection(db_name: str):
    if _DbClient.DATABASES.get(db_name) is None:
        raise Exception(f"Connection for {db_name} not created.")
    return _DbClient.DATABASES[db_name]

@asynccontextmanager
async def transaction(db_name: str) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    client = get_db_conection(db_name)
    async with await client.start_session() as session:
        yield session
