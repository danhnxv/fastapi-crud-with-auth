# Digital Asset Accounting API

## Create virtual environment
```
cd current directory
virtualenv .venv --python=python3.9
```
### Install packages
```
source .venv/bin/activate
pip install -r requirements.txt
```
### Update requirements file:
```
pip freeze > requirements.txt

```

## Copy environment
```
cp .env-example .env
```

## Run API
```
sh start-dev.sh
```

## Unitest
```
cp .env-example .test.env
pytest -x
```

### Format code - precommit
```
pip install pre-commit
pip install ruff
```

### Run docker-compose
```
cp .<ENVIRONMENT>.env .env
sh scripts/deploy.sh <ENVIRONMENT> <BRANCH>
sh scripts/stop-docker.sh <ENVIRONMENT>
```

### Default account
```
email: fastapi
password: 123456
```

### Connect to mongodb running on docker
```
docker exec -it <MONGODB_INSTANCE_ID> mongosh -u "root" -p "pwd"
```

### Backup mongodb on Docker
```
docker exec -i <CONTAINER_ID> /usr/bin/mongodump --username "root" --password "pwd" --authenticationDatabase admin --db todo --archive > todo.dump
```

### Restore mongodb to Docker
```
docker exec -i <CONTAINER_ID> /usr/bin/mongorestore --username "root" --password "pwd" --authenticationDatabase admin --nsInclude="todo.*" --archive < ~/Downloads/todo.dump
```
