# Setting up your development environment

Launch postgres

```
docker-compose up
```

Create a virtual environment

```
python -m venv venv
```

Activate your virtual environment

```
source venv/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

Connect to the database and create the `fof` database

Database migration

```
alembic -c ./db/alembic.ini -x seed=true upgrade head
```
