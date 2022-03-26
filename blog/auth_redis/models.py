from dataclasses import dataclass
from traceback import print_exception
from typing import Any, Dict

from flask_login import UserMixin
from redis import Redis
from ujson import dumps

from blog import db


@dataclass
class _UserDict():
    id: int
    username: str
    password: str
    email: str
    isAdmin: bool


@dataclass
class User(UserMixin):

    def __init__(
        self,
        _user: Dict[str, Any],
    ) -> None:
        _user = _UserDict(**_user)
        with db.pipeline() as pipe:
            pipe.get(_user.id)
            pipe.get(_user.username)

            try:
                results = pipe.execute()
                assert not all(results), "REDIS DB: user already registered"
                self.update(_user, db)
            except AssertionError as e:
                print_exception(type(e), e, e.__traceback__)
                del self
                assert False

    def assert_types(self, _payload: _UserDict):
        assert isinstance(
            _payload.id, int), \
            f"Type Assertion: type {type(_payload.id)} is not an int"
        assert isinstance(
            _payload.username, str), \
            f"Type Assertion: type {type(_payload.username)} is not a str"
        assert isinstance(
            _payload.password, str), \
            f"Type Assertion: type {type(_payload.password)} is not a str"
        assert isinstance(
            _payload.email, str), \
            f"Type Assertion: type {type(_payload.email)} is not a str"
        assert isinstance(
            _payload.isAdmin, bool), \
            f"Type Assertion: type {type(_payload.isAdmin)} is not a bool"

    def update(self, payload: _UserDict, db: Redis = None):
        self.assert_types(payload)
        self.__dict__.update(payload.__dict__)
        try:
            stripped_attr = self.__dict__
            # print(stripped_attr, "\n", payload.__dict__)
            assert db.hmset(
                "users",
                {str(payload.id): dumps(stripped_attr)}
            ), "HSET: tx failed"
            assert db.hmset(
                "usernames", payload.username, payload.id
            )
        except AssertionError as e:
            print_exception(type(e), e, e.__traceback__)
            assert False, "Execution terminated"

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def __repr__(self):
        return "<User {}>".format(self.username)
