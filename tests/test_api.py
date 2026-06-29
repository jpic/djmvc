import json

import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client(client, db):
    User = get_user_model()
    user = User.objects.create_superuser(
        username='apiuser',
        email='api@example.com',
        password='test',
    )
    client.force_login(user)
    return client


def csrf_headers(client):
    response = client.get('/item/create/')
    token = response.cookies['csrftoken'].value
    return {'HTTP_X_CSRFTOKEN': token}


@pytest.mark.django_db
def test_json_create_list_detail_update_delete(api_client):
    headers = csrf_headers(api_client)

    response = api_client.post(
        '/item/create/',
        data=json.dumps({'name': 'test item'}),
        content_type='application/json',
        **headers,
    )
    assert response.status_code == 201
    assert response.json()['status'] == 'accepted'

    response = api_client.post(
        '/item/create/',
        data=json.dumps({'name': ''}),
        content_type='application/json',
        **headers,
    )
    assert response.status_code == 405
    assert response.json()['status'] == 'invalid data'

    response = api_client.get('/item/', HTTP_ACCEPT='application/json')
    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == 1
    assert data['results'][0]['name'] == 'test item'
    pk = data['results'][0]['id']

    response = api_client.get(f'/item/{pk}/detail/', HTTP_ACCEPT='application/json')
    assert response.json() == {'id': pk, 'name': 'test item'}

    response = api_client.patch(
        f'/item/{pk}/update/',
        data=json.dumps({'name': 'updated item'}),
        content_type='application/json',
        **headers,
    )
    assert response.status_code == 201
    assert response.json()['data']['name'] == 'updated item'

    response = api_client.post(
        f'/item/{pk}/update/',
        data=json.dumps({'name': 'nope'}),
        content_type='application/json',
        **headers,
    )
    assert response.status_code == 405
    assert 'allowed_methods' in response.json()

    response = api_client.post(
        f'/item/{pk}/delete/',
        data=json.dumps({}),
        content_type='application/json',
        **headers,
    )
    assert response.status_code == 405
    assert 'allowed_methods' in response.json()

    response = api_client.delete(f'/item/{pk}/delete/', **headers)
    assert response.status_code == 200
    assert response.json()['status'] == 'deleted'


@pytest.mark.django_db
def test_schema_lists_all_json_routes_anonymously(client):
    response = client.get('/api/schema/')
    assert response.status_code == 200
    paths = response.json()['paths']
    item_paths = [path for path in paths if 'item' in path]
    assert item_paths
    assert '/api/login' in paths


@pytest.mark.django_db
def test_schema_and_swagger_ui(api_client):
    response = api_client.get('/api/schema/')
    assert response.status_code == 200

    response = api_client.get(
        '/api/schema/',
        HTTP_ACCEPT='application/json',
    )
    assert response.status_code == 200
    schema = response.json()
    assert schema['swagger'] == '2.0'
    item_paths = [path for path in schema['paths'] if 'item' in path]
    assert item_paths
    item_update_paths = [
        path for path in item_paths
        if '{pk}' in path and 'update' in path
    ]
    assert item_update_paths
    update_ops = schema['paths'][item_update_paths[0]]
    assert 'put' in update_ops
    assert 'patch' in update_ops
    assert 'delete' in str(schema['paths'])

    response = api_client.get('/api/')
    assert response.status_code == 200
    assert b'swagger-ui' in response.content