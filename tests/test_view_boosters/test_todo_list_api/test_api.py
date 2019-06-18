import requests
import json


def test_api_endpoint_existence(todolist_app):
	with todolist_app.test_client() as client:
		resp = client.get('/tasks')
		assert resp.status_code == 200

def test_user_creation(todolist_app):
	with todolist_app.test_client() as client:
		resp = client.jpost(
			'/users', {
				"name": "popeye",
				"email": "popeye@acme.com",
				"gender": "male"
			}
		)
		assert resp['status'] == 'success'
		assert 'id' in resp['result']
		assert resp['result']['id'] == 1

def test_multi_users_creation(todolist_app):   
	with todolist_app.test_client() as client:
		resp = client.jpost(
			'/users', [{
				"name": "sylvester",
				"email": "sylvester@acme.com",
				"gender": "male"
			}, {
				"name": "tweety",
				"email": "tweety@acme.com",
				"gender": "female"
			}]
		)
		assert resp['status'] == 'success'
		assert len(resp['result']) == 2

def test_task_creation(todolist_app):
	with todolist_app.test_client() as client:
		resp = client.jpost(
			'/tasks', {
				"title": "Eat spinach",
				"user_id": 1
			}
		)
		assert resp['status'] == 'success'
		assert 'id' in resp['result']
		assert resp['result']['id'] == 1

def test_multi_tasks_creation(todolist_app):
	with todolist_app.test_client() as client:
		resp = client.jpost(
			'/tasks', [{
				"title": "Eat tweety",
				"user_email": "sylvester@acme.com"
			}, {
				"title": "Solve a mystery",
				"user_email": "tweety@acme.com"
			}]
		)
		assert resp['status'] == 'success'


def test_task_updation(todolist_app):
	with todolist_app.test_client() as client:
		modified_title = "Eat spinach from tin"
		resp = client.jput(
			'/tasks/1', {
				"title": modified_title
			}
		)
		assert resp['status'] == 'success'
		assert 'id' in resp['result']
		assert resp['result']['title'] == modified_title

def test_tasks_index(todolist_app):
	with todolist_app.test_client() as client:
		resp = client.jget('/tasks')
		assert resp['status'] == 'success'
		assert resp['result'][0]['id'] == 1

def test_task_get(todolist_app):
	with todolist_app.test_client() as client:
		resp = client.jget('/tasks/1')
		assert resp['status'] == 'success'
		assert resp['result']['id'] == 1

def test_task_filtering(todolist_app):
	with todolist_app.test_client() as client:
		resp = client.jget('/tasks?user_email=tweety@acme.com')
		assert resp['status'] == 'success'
		assert resp['result'][0]['title'] == "Solve a mystery"

