from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.to_do_crud.urls import todo_router
from database import initialize_mongo_connection
from app.config import Config

def attach_middleware(app: FastAPI):
    origins = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

async def create_app():
    app = FastAPI()
    attach_middleware(app)
    app.include_router(todo_router)
    @app.on_event("startup")
    async def init_database():
        from run import Main
        loop = Main.get_running_event_loop()
        initialize_mongo_connection(
            {
                "databases": Config.MONGO_DATABASES,
                "loop": loop,
                "app_name": "todo_app"
            }
        )
        # added just ot create indexes for first time
        # from database.mongo.base_model import Indexes
        # await Indexes.create_indexes()

    
    @app.api_route("/_healtz")
    async def health_check():
        return {"ok": "ok"}
    return app
