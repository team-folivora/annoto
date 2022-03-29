![build api](https://github.com/team-folivora/annoto/actions/workflows/build-api.yml/badge.svg?branch=main)

![build static](https://github.com/team-folivora/annoto/actions/workflows/build-static.yml/badge.svg?branch=main)

[![codecov](https://codecov.io/gh/team-folivora/annoto/branch/main/graph/badge.svg?token=8OKTHCXOEA)](https://codecov.io/gh/team-folivora/annoto)

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

## Testing and Linting

* `mypy -p api`, `pylint api`, `python -m pytest .`, `python -m pytest --cov .`

* `npm run lint`, `npm run test:e2e`, `npm run test:unit`
