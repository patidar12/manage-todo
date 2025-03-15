import json
from fastapi import APIRouter, Request, Response
from database.mongo.models import ToDoCollection

router = APIRouter(prefix="/todo")

class ToDoCrud:
    @router.get("/{title}")
    async def get_todo_by_id(request: Request, title: str):
        todo = await ToDoCollection.connect().find_one({"title": title})
        todo = ToDoCollection.SCHEMA().dump(todo)
        return Response(json.dumps(todo, default=str), status_code=200)

    @router.get("/")
    async def get_all_todo(request: Request):
        all_todos = ToDoCollection.connect().find()
        all_todos = [todo async for todo in all_todos]
        all_todos = ToDoCollection.SCHEMA(many=True).dump(all_todos)
        return Response(content=json.dumps(all_todos, default=str), status_code=200)

    @router.post("/")
    async def create_toto(request: Request):
        data: dict = ToDoCollection.SCHEMA().load(json.loads(await request.body()))
        await ToDoCollection.connect().insert_one(data)
        return Response(content=json.dumps(data, default=str), status_code=200)

    @router.put("/{title}")
    async def update_todo(request: Request, title: str):
        data: dict = json.loads(await request.body())
        data = ToDoCollection.SCHEMA().load(data)
        await ToDoCollection.connect().update_one({"title": title}, {"$set": data})
        return Response(content=json.dumps(data, default=str), status_code=200) 

    @router.delete("/{title}")
    async def delete_todo(request: Request, title: str):
        await ToDoCollection.connect().delete_one({"title": title})
        data  = {"title": title, "message": "Todo Deleted Succesfully"}
        return Response(content=json.dumps(data, default=str), status_code=200)