![build api](https://github.com/team-folivora/annoto/actions/workflows/build-api.yml/badge.svg?branch=main)
![build static](https://github.com/team-folivora/annoto/actions/workflows/build-static.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/team-folivora/annoto/branch/main/graph/badge.svg?token=8OKTHCXOEA)](https://codecov.io/gh/team-folivora/annoto)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)



# annoto

Medical annotation tool

# Live Demo

## Dev

* [http://dev.folivora.online/](http://dev.folivora.online/) ([Api](http://api.dev.folivora.online/))

# Setup

* Install `python3`, `node`, `npm`, `nvm`

* `cd static; nvm use; npm i; npm run lint`

* `cd api; pip install -r requirements.txt`

## For development

* `cd api; pip install -r requirements-dev.txt`

# Run

* `cd api; python -m mod`

* `cd static; npm run dev`

## Testing and Linting

* `mypy mod`,`pylint mod`, `pytest mod`, `pytest mod --cov`

* `npm run lint`, `npm run test:e2e`, `npm run test:unit`

# Docker

* Execute `run-dev.sh` to setup and start a dedicated development container.
    * Add the `--local-data-dir` argument if you want to mount your local `~/.annoto` folder into the container
* Execute `connect-dev.sh` to open a new bash inside the (already running) development container.
