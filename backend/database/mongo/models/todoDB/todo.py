from typing import List, Tuple
from marshmallow import Schema

from pymongo import IndexModel, ASCENDING
from database.mongo.validators.todoDB.todo import ToDoSchema
from database.mongo.base_model import MongoModel

class ToDoCollection(MongoModel):
    DB: str = "todoDB"
    COLLECTION: str = "todo"
    SCHEMA: Schema = ToDoSchema
    INDEX_LIST: tuple = [
        IndexModel(
            [
                ('title', ASCENDING)
            ],
            background=True,
            #unique=True
        )
    ]

