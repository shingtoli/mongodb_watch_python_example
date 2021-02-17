## MongoDB Watch Python Example ##

Instead of polling the Database, its possible to use the [Change Streams](https://docs.mongodb.com/manual/changeStreams/) feature in MongoDB to subscribe to changes in the database.

This program is a Flask Server that can be accessed on [localhost:5000](http://127.0.0.1:5000/)

The GET `/tasks` API only reads from a `dict` and does not access the Database with a find call, instead a Stream subscription on a separate Python `Thread` updates the `dict` on any change to the subscribed MongoDB Collection.

Install [MongoDB](https://www.mongodb.com)

Add to `/etc/mongod.conf`
```
replication:
  replSetName: rs0
```

Run `rs.initiate()` in mongo shell
```sh
mongo
> rs.initiate()
```

Install [Poetry](python-poetry.org)

```sh
poetry install
```

Run this program by
```sh
python app/main.py
```

Run unit tests with
```sh
python -m unittest discover app/tests
```
