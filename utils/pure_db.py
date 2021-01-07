import asyncio

from databases import Database
from utils.const import DB_URL
from utils.orm_db import authors


async def connect_db():
    db = Database(DB_URL)
    await db.connect()
    return db


async def disconnect_db(db):
    await db.disconnect()


async def execute(query, is_many, values=None):
    db = await connect_db()

    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

    await disconnect_db(db)


async def fetch(query, is_one, values=None):
    db = await connect_db()
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        out = []
        for row in result:
            out.append(dict(row))
    await disconnect_db(db)

    return out

# insert_query = "insert into books values(:custom, :name, :author, :year)"
# insert_values = [
#     {"custom": "isbn1", "name": "book1", "author": "author1", "year": 2019},
#     {"custom": "isbn2", "name": "book2", "author": "author2", "year": 2018},
#     {"custom": "isbn3", "name": "book3", "author": "author3", "year": 2017}
# ]
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(execute(insert_query, True, insert_values))

# select_query = "select * from books where isbn=:isbn"
# values = {"isbn": "isbn2"}
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(fetch(select_query, True, values))

# select_all_query = "select * from books"
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(fetch(select_all_query, False))


# async def test_orm():
#     # insert_query = authors.insert().values(id=1, name="author1", books=["book1", "book2"])
#     # await execute(insert_query, False)
#     select_query = authors.select().where(authors.c.id==2)
#     await fetch(select_query, True)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test_orm())