# README

Flask tutorial, creates a simple blog with Flask and a SQLite database. I followed this tutorial because I wanted to learn Flask.
* Official tutorial page: https://flask.palletsprojects.com/en/1.1.x/
* Official example page: https://github.com/pallets/flask/tree/master/examples/tutorial

I haven't deployed it yet, just wanted to play with it.

## Changes from official tutorial

I have modified some things, for example I wasn't happy with having the same method be used for GET and POST and separating logic for each with conditionals, I think it is much cleaner to have separate GET and POST methods instead (I'm very conditional-averse, but this is a clear case where there is absolutely no need for this conditionals).

The register and login logic seemed to be two completely separated concepts, but they were smashed into the same module. I separated them into two modules `register` and `login` and namespaced them inside `auth`.

Another thing that bothered me was the database implementation details spread all over the codebase, calls to `execute` on `db` with SQL statements in view. If I was to switch to Postgres instead of SQLite, I would have to change a lot of files. There is no need to do this because we already have a `db` module where we can encapsulate the implementation details of whatever database we choose to use.

Regarding the tests, some of them had several assertions in the same test. I had some tests failing and it was a pain to see what exactly was wrong. There was untested logic too. So I separated the tests into granular assertions and added test coverage where missing. I am not a fan of parametrized tests either, but I left the ones that made sense.

There is this thing where as you develop a codebase, your tests get more and more specific, while your production code gets more and more generic. I found the tests generic and not very documenting. Test descriptions like `test_update` and similar don't tell me much about what update does.

Finally, I missed grouping tests like one can do in RSpec using `describe` or `context`. When using unittest you can at least group them in classes, that's the closest I've found. But pytest doesn't seem to support grouping tests in classes, unless you use unittest classes. I'd prefer to not mix two testing frameworks.

There are still things I want to change, but this is a first stab at it.


## Install

```sh
git clone git@github.com:octopusinvitro/flask-tutorial.git
cd flask-tutorial

python3 -m venv venv
pip install --upgrade pip
pip install -e .
```


## Run

Copy `.env-editme` to `.env` and replace your app's values. Then load them into the environment, for example:

```sh
. .env
```

Then initialize the database. This will create an `instance` folder under your root directory with a sqlite database inside. Finally, run flask.

```sh
flask init-db
flask run
```

You can now open <http://localhost:5000> in a browser.


## Run tests

Run all:
```sh
pytest -v
```

Run one file:
```sh
pytest tests/test_example.py
```

Run one test in a file:
```sh
pytest tests/test_example.py::test_thistest
pytest tests/test_example.py Example.test_thistest
```

Run coverage:
```sh
coverage run --omit 'venv/*' -m pytest
```

See coverage
```sh
coverage report
```

or:
```sh
coverage html
firefox htmlcov/index.html
```

## Debug

```python
import ipdb; ipdb.set_trace()
```


## Deploy
```sh
pip install wheel
python3 setup.py bdist_wheel
```

Upload the whl file to your server, and then:

```sh
python3 -m venv venv

pip install --upgrade pip
pip install flaskr-1.0.0-py3-none-any.whl
```

Then change your secret key:
```sh
echo "SECRET_KEY = $(python -c 'import os; print(os.urandom(16))')" > venv/var/flaskr-instance/config.py
```

Then serve!
```sh
export FLASK_APP=flaskr
flask init-db

pip install waitress
waitress-serve --call 'flaskr:create_app'
```


## To do

- [x] refactor sqlite implementation details out of the controllers
- [ ] If login fails, display link to register.
- [ ] Have the blog under blog and static pages under /
- [ ] Put data.sql under `fixtures/`
- [ ] Instead of loading data.sql in tests, explicitly create records in every test.


### Features from tutorial

- [ ] A detail view to show a single post. Click a post’s title to go to its page.
- [ ] Like / unlike a post.
- [ ] Comments.
- [ ] Tags. Clicking a tag shows all the posts with that tag.
- [ ] A search box that filters the index page by name.
- [ ] Paged display. Only show 5 posts per page.
- [ ] Upload an image to go along with a post.
- [ ] Format posts using Markdown.
- [ ] An RSS feed of new posts.
