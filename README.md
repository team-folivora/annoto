![build api](https://github.com/team-folivora/annoto/actions/workflows/build-api.yml/badge.svg?branch=main)
![build static](https://github.com/team-folivora/annoto/actions/workflows/build-static.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/team-folivora/annoto/branch/dev/graph/badge.svg?token=8OKTHCXOEA)](https://codecov.io/gh/team-folivora/annoto)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)



# annoto

Medical annotation tool

# Live Demo

## Dev

* [http://dev.folivora.online/](http://dev.folivora.online/) ([Api](http://api.dev.folivora.online/))

# Setup

* Install `python3`, `node`, `npm`, `nvm`

* Frontend: `cd static; nvm use; npm i; npm run lint`

* Backend: `cd api; python3 manage.py install {dev}`

# Run

* Backend: `cd api; python3 manage.py run`

* Frontend: `cd static; npm run dev`

## Testing, Linting and Formatting

* Backend Full build: `python3 manage.py build`

* Backend Only tests: `python3 manage.py test {--cov}`

* Backend Format: `python3 manage.py format`

* Frontend: `npm run lint`, `npm run test:e2e`, `npm run test:unit`

## Database

* Create database: `python3 manage.py db-create`

* Load test data into database: `python3 manage.py db-reload`

* Dump database content into JSON-file: `python3 manage.py data-dump`

* Delete and recreate database: `python3 manage.py db-reset`

* Create new Migration: `python3 manage.py migration-create`

* Apply (new) Migrations: `python3 manage.py migration-apply`

# Docker

* Execute `run-dev.sh` to setup and start a dedicated development container.
    * Add the `--local-data-dir` argument if you want to mount your local `~/.annoto` folder into the container
* Execute `connect-dev.sh` to open a new bash inside the (already running) development container.
* Execute `exit-dev.sh` to stop the development container.
