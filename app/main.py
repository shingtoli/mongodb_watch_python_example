import json
from time import sleep
from copy import deepcopy
from threading import Thread
from flask import Flask, request, jsonify
from pymongo import MongoClient


def watch(collection, store):
    with collection.watch() as stream:
        for change in stream:
            print(change)
            if change['operationType'] in ['insert']:
                store[change['documentKey']['_id']] = change['fullDocument']
            sleep(0.002)

def start_watch_thread(collection, store):
    watch_thread = Thread(target=watch, args=(collection, store))
    watch_thread.daemon = True
    watch_thread.start()
    return watch_thread

def getCollection(name):
    client = MongoClient(replicaSet='rs0')
    db = client.example
    return db[name]

def create_app(collection, tasks):
    app = Flask(__name__)

    @app.route('/tasks', methods=['GET'])
    def fetch_tasks():
        output = []
        for task in tasks.values():
            copied_task = deepcopy(task)
            copied_task['_id'] = str(copied_task['_id'])
            output.append(copied_task)
    
        return jsonify(output)

    @app.route('/tasks', methods=['POST'])
    def create_tasks():
        new_tasks = json.loads(request.data)
        result = collection.insert_many(new_tasks)
        return jsonify({'inserted_ids': [str(id) for id in result.inserted_ids]})

    return app


def main():
    collection = getCollection('tasks')
    # Memory store for tasks
    tasks = {str(task['_id']): task for task in collection.find(filter={})} or {}

    app = create_app(collection, tasks)
    start_watch_thread(collection, tasks)
    
    app.run()

if __name__ == '__main__':
    main()
