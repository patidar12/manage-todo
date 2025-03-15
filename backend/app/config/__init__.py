from pymongo import ReadPreference

class Config(object):
    MONGO_DATABASES = {
        "todoDB": {
            "host": "mongodb://127.0.0.1:27017/todoDB?directConnection=true", # args.mongo_todoDb_read_only
            "read_preference": ReadPreference.SECONDARY_PREFERRED
        },
        "todoDB_primary": {
            "host": "mongodb://127.0.0.1:27017/todoDB?directConnection=true", # args.mongo_todoDb_read_write
            "read_preference": ReadPreference.PRIMARY
        }
    }