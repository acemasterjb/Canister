import os
import tempfile

import pytest

from blog import create_app, init_db


db_fd, db_path = tempfile.mkstemp()

app = create_app({
    'TESTING': True,
    'DATABASE': db_path,
})


@pytest.fixture
def client():
    client = app.test_client()

    with app.app_context():
        init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data


# def test_messages(client):
#     """Test that messages work."""

#     login(client, app.config['USERNAME'], app.config['PASSWORD'])
#     rv=client.post('/create', data=dict(
#         title='<Hello>',
#         body='<strong>HTML</strong> allowed here'
#     ), follow_redirects=True)
#     assert b'No entries here so far' not in rv.data
#     assert b'&lt;Hello&gt;' in rv.data
#     assert b'<strong>HTML</strong> allowed here' in rv.data
