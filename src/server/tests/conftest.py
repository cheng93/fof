import contextlib
import pytest
from collections import namedtuple

class FakeCursor():
    def __init__(self, result):
        self.result = result

    async def fetchall(self):
        return self.result

    async def first(self):
        return self.result[0]

class FakeDbConnection():
    def __init__(self, store):
        self.store = store

    async def __aenter__(self):
        return self.store

    async def __aexit__(self, exc_type, exc, tb):
        self.store.reset()

class Row():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class QueryStore():
    def __init__(self):
        self.store = {}
    
    def register_query(self, query, result):
        self.store[str(query)] = ([Row(**r) for r in result] 
                                    if isinstance(result, list)
                                    else [Row(**result)])

    async def execute(self, query):
        return FakeCursor(self.store[str(query)])

    def reset(self):
        self.store = {}

class FakeDb():
    def __init__(self):
        self.store = QueryStore()

    def acquire(self):
        return FakeDbConnection(self.store)

    def register_query(self, query, result):
        self.store.register_query(query, result)

@pytest.fixture
def mock_db():
    return FakeDb()