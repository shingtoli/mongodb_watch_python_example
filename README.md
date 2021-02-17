## MongoDB Watch Python Example ##


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

Run this program by
```sh
python src/main.py
```
