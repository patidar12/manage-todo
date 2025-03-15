from typing import List
from pymongo import ReadPreference
from pymongo.collection import Collection
from database.mongo import _DbClient
from database.mongo.validators import BaseValidatorSchema

class Indexes:
    """
    Global index Mapping
    """
    _INDEX_LIST = {}
    @classmethod
    def add_index(cls, db: str, collection: str, indexes: str):
        cls._INDEX_LIST[(db, collection)] = indexes
    
    @classmethod
    async def create_indexes(cls, collections: List[str] = None):
        for db_collection, index_list in cls._INDEX_LIST.items():
            db, collection = db_collection

            if collections and collection not in collections:
                print({"skipping": collection})
                continue
            db_model: Collection = _DbClient.DATABASES[db][collection]
            index_resp = await db_model.create_indexes(index_list)
            print(
                {
                    "db": db,
                    "collection": collection,
                    "resp": index_resp
                }
            )
                

class Base(type):
    def __new__(cls, name, base, body, *args, **kwargs):
        if name not in ('MongoModel'):
            db = body.get("DB")
            collection = body.get("COLLECTION")
            index_list = body.get("INDEX_LIST") or []
            assert isinstance(db, str), f"Not a valid db: {db} name for: {name}"
            assert isinstance(collection, str), f"Not a valid collection: {collection} name for {name}"
            if index_list:
                assert isinstance(
                    index_list, (list, tuple)
                ), f"Not a valid list of indexes for {name} model."
                Indexes.add_index(db, collection, index_list)
        return super().__new__(cls, name, base, body, *args, **kwargs)

class MongoModel(metaclass=Base):
    DB: str
    COLLECTION: str
    INDEX_LIST: tuple
    SCHEMA: BaseValidatorSchema
    @classmethod
    def connect(cls, primary=False):
        if _DbClient.DATABASES.get(cls.DB) is None:
            raise Exception(f"Connection for {cls.DB} not found")
        collection: Collection = _DbClient.DATABASES[cls.DB][cls.COLLECTION]
        if primary:
            return collection.with_options(read_preference=ReadPreference.PRIMARY)
        return collection
    
    @classmethod
    def serialize(cls, data: dict) -> dict:
        return cls.SCHEMA().dump(data)
    
    @classmethod
    async def get_latest_uid(cls):
        records = cls.connect(primary=True).find({}).sort({"uid": -1}).limit(1)
        async for record in records:
            return record.get("uid") + 1
        return 1
    @classmethod
    async def insert_and_get_document(cls, data: dict) -> dict:
        resp = await cls.connect().insert_one(data)
        data.update({"_id": resp.inserted_id})
        return data
    # TODO: all the operation that is common for all the collection can be added here.