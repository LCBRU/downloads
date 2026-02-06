# -*- coding: utf-8 -*-
"""
    LCBRU Downloads Tests
"""

import pytest
import downloads
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import TestConfig, TestConfigCRSF
from downloads.models import Download
from downloads.database import db as _db
from sqlalchemy import select, func


class Tureen(BeautifulSoup):

    def find_text_input(self, name):
        return self.find_input(name, 'text')

    def find_checkbox_input(self, name):
        return self.find_input(name, 'checkbox')

    def find_hidden_input(self, name):
        return self.find_input(name, 'hidden')

    def find_input(self, name, type):
        return super(self.__class__, self).find(
            lambda tag: tag.name == 'input' and
            tag['id'] == name and
            tag['name'] == name and
            tag['type'] == type
        )


@pytest.fixture(scope='session')
def app(request):
    app = downloads.create_app(TestConfig)
    ctx = app.app_context()
    ctx.push()

    return app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.yield_fixture(scope='function')
def db(app, request):

    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.yield_fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session()

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.yield_fixture(scope='function')
def client_with_crsf(request):
    app = downloads.create_app(TestConfigCRSF)
    app.app_context().push()
    client = app.test_client()

    yield client


@pytest.mark.parametrize("path", [
    ('/uihfihihf'),
    ('/submitted/igfiugrigii'),
    ('/download/igfiugrigii')
])
def test_missing_route(client, session, path):
    resp = client.get(path)
    assert resp.status_code == 404


@pytest.mark.parametrize("path", [
    ('/'),
    ('/static/css/main.css'),
    ('/request')
])
def test_url_exists(client, path):
    resp = client.get(path)

    assert resp.status_code == 200


@pytest.mark.parametrize("path", [
    ('/'),
    ('/request')
])
def test_html_boilerplate(client, path):
    resp = client.get(path)
    rsoup = BeautifulSoup(resp.data, 'html.parser')

    assert rsoup.find('html') is not None
    assert rsoup.find('html')['lang'] == "en"
    assert rsoup.find('head') is not None
    assert rsoup.find(
        lambda tag: tag.name == "meta" and
        tag.has_attr('charset') and
        tag['charset'] == "utf-8"
    ) is not None
    assert rsoup.title is not None
    assert rsoup.find('body') is not None
    assert rsoup.find('title') is not None


@pytest.mark.parametrize("path", [
    ('/request')
])
def test_form_boilerplate(client_with_crsf, path):
    resp = client_with_crsf.get(path)
    rsoup = Tureen(resp.data, 'html.parser')

    assert rsoup.find('form') is not None
    assert rsoup.find('form')['method'] == "POST"
    csrf = rsoup.find_hidden_input('csrf_token')
    assert csrf is not None
    assert csrf['value'] != ''


def test_download_form_contents(client_with_crsf):
    resp = client_with_crsf.get('/request')
    rsoup = Tureen(resp.data, 'html.parser')

    assert rsoup.find_text_input('title') is not None
    assert rsoup.find_text_input('first_name') is not None
    assert rsoup.find_text_input('last_name') is not None
    assert rsoup.find_text_input('institution') is not None
    assert rsoup.find_checkbox_input('scientific_purposes_only') is not None


@pytest.mark.parametrize(
    "title,first_name,last_name,institution,scientific_purposes_only", [
        ('Mr', 'Richard', 'Bramley', 'LCBRU', 'y'),
        ('a' * 50, 'b' * 100, 'c' * 100, 'd' * 500, 'y')
    ])
def test_download_form_submission(
        client, session, title, first_name, last_name, institution,
        scientific_purposes_only):
    resp = client.post('/request', data=dict(
        title=title,
        first_name=first_name,
        last_name=last_name,
        institution=institution,
        scientific_purposes_only=scientific_purposes_only
    ), follow_redirects=False)

    assert resp.status_code == 302

    assert urlparse(resp.location).path.startswith('/submitted/')
    assert db.session.execute(select(func.count(Download))).scalar_one() == 1

    actual = db.session.execute(select(Download)).scalar_one()
    assert actual.title == title
    assert actual.first_name == first_name
    assert actual.last_name == last_name
    assert actual.institution == institution
    assert actual.scientific_purposes_only

    submitted = client.get('/submitted/{}'.format(actual.id))
    assert submitted.status_code == 200

    download = client.get('/download/{}'.format(actual.id))
    assert download.status_code == 200


@pytest.mark.parametrize(
    "title,first_name,last_name,institution,scientific_purposes_only", [
        ('Mr', 'Richard', 'Bramley', 'LCBRU', None),
        ('', 'Richard', 'Bramley', 'LCBRU', 'y'),
        ('Mr', '', 'Bramley', 'LCBRU', 'y'),
        ('Mr', 'Richard', '', 'LCBRU', 'y'),
        ('Mr', 'Richard', 'Bramley', '', 'y'),
        ('a' * 51, 'b' * 100, 'c' * 100, 'd' * 500, 'y'),
        ('a' * 50, 'b' * 101, 'c' * 100, 'd' * 500, 'y'),
        ('a' * 50, 'b' * 100, 'c' * 101, 'd' * 500, 'y'),
        ('a' * 50, 'b' * 100, 'c' * 100, 'd' * 501, 'y')
    ])
def test_download_form_submission_not_scientific(
        client, session, title, first_name, last_name, institution,
        scientific_purposes_only):
    resp = client.post('/request', data=dict(
        title=title,
        first_name=first_name,
        last_name=last_name,
        institution=institution,
        scientific_purposes_only=scientific_purposes_only
    ), follow_redirects=False)

    assert resp.status_code == 200

    assert db.session.execute(select(func.count(Download))).scalar_one() == 0
