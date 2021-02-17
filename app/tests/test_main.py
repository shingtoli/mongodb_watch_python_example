from time import sleep
from unittest import TestCase
from app.main import getCollection, create_app, start_watch_thread

class TestMongoWatch(TestCase):
    def setUp(self):
        # Clear test data
        collection = getCollection('tasks')
        collection.delete_many(filter={})
        self.collection = collection
        self.tasks = {}
        self.app = create_app(self.collection, self.tasks).test_client()
        self.thread = start_watch_thread(collection, self.tasks)

    def tearDown(self):
        self.thread.join(0)

    def test_create_and_fetch(self):
        task_to_create = {
            "name": "Do homework",
            "due_date": "2077-08-01 15:35:08"
        }
        create_response = self.app.post('/tasks', json=[task_to_create])
        self.assertEqual(create_response.status_code, 200)
        inserted_ids = create_response.json['inserted_ids']
        self.assertEqual(len(inserted_ids), 1)

        sleep(0.02)
        print(self.tasks)

        fetch_response= self.app.get('/tasks')
        self.assertEqual(fetch_response.status_code, 200)
        task_to_create['_id'] = inserted_ids[0]
        fetch_data = fetch_response.json
        print(fetch_data)
        self.assertTrue(len(fetch_data) > 0)
        self.assertDictEqual(fetch_data[0], task_to_create)
