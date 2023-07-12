# Setting up

In order to config the database connection, the following ENV variables needs to be set up:
```
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

# Migrate DB
```
python manage.py makemigrations
python manage.py migrate
```

# Create admin
```
python manage.py createsuperuser --email admin@example.com --username admin
```

# API instructions

## Get all dynamic models in the system

### URL:
GET: http://127.0.0.1:8000/api/table/

### Response:
Response returns a list of all dynamic models currently available.
```
[
    {
        "pk": 1,
        "name": "table_1"
    },
    {
        "pk": 2,
        "name": "table_2"
    }
]
```

## Create new model
### URL:
POST: http://127.0.0.1:8000/api/table/

### Request:
Request must contain the model that we want to create.
```
{
    "name": "table_3",
    "columns": [{
        "name": "first_column",
        "type": "INTEGER"
    },
    {
        "name": "second_column",
        "type": "STRING"
    }]
}
```

### Response:
Response returns the model that was created or an error if it occurs.
```
{
    "name": "table_3",
    "columns": [{
        "name": "first_column",
        "type": "INTEGER"
    },
    {
        "name": "second_column",
        "type": "STRING"
    }]
}
```

## Update existing model
### URL:
http://127.0.0.1:8000/api/table/<pk>/

### Request:
Request must contain the new model definition.
```
{
    "name": "table_3_renamed",
    "columns": [{
        "name": "first_column",
        "type": "INTEGER"
    },
    {
        "name": "second_column",
        "type": "STRING"
    },
    {
        "name": "third_column",
        "type": "STRING"
    }]
}
```

### Response:
Response returns the new model definition or an error it updates failed.
```
{
    "name": "table_3_renamed",
    "columns": [{
        "name": "first_column",
        "type": "INTEGER"
    },
    {
        "name": "second_column",
        "type": "STRING"
    },
    {
        "name": "third_column",
        "type": "STRING"
    }]
}
```