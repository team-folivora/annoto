# annoto
Medical annotation tool

# Setup
* Install `python3`, `python3-flask`, `node`, `npm`, `nvm`

* `cd static/annoto; nvm use; npm i; npm run lint`

* `cd api; pip install -r requirements.txt`

## For development

* `cd api; pip install -r requirements-dev.txt`

# Run

* `cd api; FLASK_ENV="development" flask run`

* `cd static/annoto; npm run dev`

## For development

* `pylint .`, `pytest`

* `npm run lint`, `npm run test:e2e`, `npm run test:unit`
