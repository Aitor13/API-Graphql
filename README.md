# Social Network API

Social Network API with Graphql, Django and JWT for authentication


### Requirements 📋

 - Python3.8 + pip
 - Docker

### Installation 🔧

Create your personal directory and clone this project inside:

```
git clone https://github.com/Aitor13/Social-Network-Api-Graphql-Django.git
```

Create a virtual environment inside you personal directory and start it:

```
virtualenv venv
source venv/bin/activate
```

Install the project requirements:

```
pip install -r requirements.txt
```

Finally start database container with the docker-compose file project:

```
docker-compose up
```

## Starting 📦

Apply django migrations:

```
python manage.py makemigrations
python manage.py migrate
```

Run the server for testing:

```
python manage.py runserver --settings socialnetwork.settings_dev
```
Load some test data:

```
python manage.py loaddata users.json
```


Validate the loaded data with this query that return all the users:

```
query {
  users {
    edges {
      node {
        username,
        archived,
        verified,
        email,
        secondaryEmail,
      }
    }
  }
}
```
## Example for create user and set any requests

Set this mutation to create user:

```
mutation {
  register(
    email: "new_user@email.com",
    username: "new_user",
    password1: "supersecretpassword",
    password2: "supersecretpassword",
  ) {
    success,
    errors,
    token,
  }
}
```

### Important

This request return the token that you must pass in all your requests with the follow header:

```
{Authorization: JWT <token>}
```

Is needed specific app for testing the next requests like a Postman

Enjoy!
