![build api](https://github.com/team-folivora/annoto/actions/workflows/build-api.yml/badge.svg?branch=main)
![build static](https://github.com/team-folivora/annoto/actions/workflows/build-static.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/team-folivora/annoto/branch/main/graph/badge.svg?token=8OKTHCXOEA)](https://codecov.io/gh/team-folivora/annoto)

# annoto

Medical annotation tool

# Setup

* Install `python3`, `node`, `npm`, `nvm`

* `cd static; nvm use; npm i; npm run lint`

* `cd api; pip install -r requirements.txt`

## For development

* `cd api; pip install -r requirements-dev.txt`

# Run

* `cd api; uvicorn mod.src.app:APP --reload`

* `cd static; npm run dev`

## Testing and Linting

* `mypy mod`,`pylint mod`, `pytest mod`, `pytest --cov mod`

* `npm run lint`, `npm run test:e2e`, `npm run test:unit`
