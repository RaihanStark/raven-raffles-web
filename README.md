# Raven Raffles

![Python Testing](https://github.com/RaihanStark/raven-raffles-web/workflows/Python%20Testing/badge.svg?branch=master&event=push)

## Setting up

##### Initialize a virtual environment

Windows:

```
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

##### Add Environment Variables

Create a file called `config.env` that contains environment variables. **Very important: do not include the `config.env` file in any commits. This should remain private.** You will manually maintain this file locally, and keep it in sync on your host.

Variables declared in file have the following format: `ENVIRONMENT_VARIABLE=value`. You may also wrap values in double quotes like `ENVIRONMENT_VARIABLE="value with spaces"`.

1. In order for Flask to run, there must be a `SECRET_KEY` variable declared. Generating one is simple with Python 3:

   ```
   $ python3 -c "import secrets; print(secrets.token_hex(16))"
   ```

   This will give you a 32-character string. Copy this string and add it to your `config.env`:

   ```
   SECRET_KEY=Generated_Random_String
   ```

2. The mailing environment variables can be set as the following.
   We recommend using [Sendgrid](https://sendgrid.com) for a mailing SMTP server, but anything else will work as well.

   ```
   MAIL_USERNAME=SendgridUsername
   MAIL_PASSWORD=SendgridPassword
   ```

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Other dependencies for running locally

You need [Redis](http://redis.io/), and [Sass](http://sass-lang.com/). Chances are, these commands will work:

**Sass:**

```
$ gem install sass
```

**Redis:**

_Mac (using [homebrew](http://brew.sh/)):_

```
$ brew install redis
```

_Linux:_

```
$ sudo apt-get install redis-server
```

You will also need to install **PostgresQL**

_Mac (using homebrew):_

```
brew install postgresql
```

_Linux (based on this [issue](https://github.com/hack4impact/flask-base/issues/96)):_

```
sudo apt-get install libpq-dev
```

##### Create the database

```
$ python manage.py recreate_db
```

##### Other setup (e.g. creating roles in database)

```
$ python manage.py setup_dev
```

Note that this will create an admin user with email and password specified by the `ADMIN_EMAIL` and `ADMIN_PASSWORD` config variables

##### [Optional] Add fake data to the database

```
$ python manage.py add_fake_data
```

## Running the app

```
$ source env/bin/activate
$ honcho start -e config.env -f Local
```
