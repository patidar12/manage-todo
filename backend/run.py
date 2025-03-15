import asyncio
import uvicorn

from app.create_app import create_app


class Main:
    _EVENT_LOOP = asyncio.get_event_loop()
    @classmethod
    def get_running_event_loop(cls) -> asyncio.events.AbstractEventLoop:
        return cls._EVENT_LOOP 

def exec():
    loop = Main.get_running_event_loop()
    app = loop.run_until_complete(create_app())
    uvicorn.run(app)



if __name__ == "__main__":
    exec() 