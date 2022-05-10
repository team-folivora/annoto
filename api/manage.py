"""This script provides basic utility commands for managing the API"""

import os
import sys

from mod.src.settings import Path


def install():
    """Installs all python requirements. Also installs dev-requirements when argument 'dev' is provided."""
    os.system("pip install -r requirements.txt")
    if len(sys.argv) == 3:
        if (sys.argv[2]) == "dev":
            os.system("pip install -r requirements-dev.txt")


def run():
    """Starts the backend"""
    os.system("python -m mod")


def run_linter():
    """Runs linter"""
    os.system("pylint mod")


def run_tests():
    """Runs pytest and provides coverage information when '--cov' is provided"""
    if len(sys.argv) >= 3:
        os.system(f"pytest mod {' '.join(sys.argv[2:])}")
    else:
        os.system("pytest mod")


def run_typecheck():
    """Runs typecheck"""
    os.system("mypy mod")


def run_linter():
    """Runs linter"""
    os.system("pylint mod")


def format():
    """Formats API as specified from GitHub CI"""
    os.system("black . & isort .")


def build():
    """Builds API as specified from GitHub CI"""
    os.system("mypy mod & pylint mod & pytest mod --cov")


def clear_db():
    """Clears database entries but keeps tables"""
    from scripts import empty_db_tables

    empty_db_tables.empty_db()


def reload_db_data():
    """Clears database entries and loads test data"""
    from scripts import load_test_data

    clear_db()
    load_test_data.load()


def create_db():
    """Creates a database file, applies all available migrations and loads the test data"""
    from scripts import load_test_data

    apply_migration()
    load_test_data.load()


def reset_db():
    """Deletes and recreates database with test data"""
    os.remove(Path.home().joinpath(".annoto").joinpath("db.sqlite3"))
    create_db()


def dump_db_data():
    """Dumps all entries from the database into 'test_data.json'"""
    from scripts import dump_data

    dump_data.dump()


def create_migration():
    """Creates a database migration with alembic"""
    os.system("alembic revision --autogenerate")
    print(
        "Be sure to proofread the autogenerated migration! After that, the migration can be applied with the 'migration-apply'-command"
    )


def apply_migration():
    """Applies a database migration with alembic"""
    os.system("alembic upgrade head")


def dump_api():
    """Dumps API"""
    os.system("PYTHON_ENV=production python3 -m mod.__dumpapi__")


def print_commands():
    """Prints available commands"""
    print("No command provided. Available commands: ")
    for key in commands.keys():
        print(f"{key}: {commands[key].__doc__}")


commands = {
    "install": install,
    "run": run,
    "test": run_tests,
    "typecheck": run_typecheck,
    "lint": run_linter,
    "format": format,
    "build": build,
    "db-dump": dump_db_data,
    "db-create": create_db,
    "db-clear": clear_db,
    "db-reload": reload_db_data,
    "db-reset": reset_db,
    "migration-create": create_migration,
    "migration-apply": apply_migration,
    "dump-api": dump_api,
    "--help": print_commands,
}

if len(sys.argv) == 1:
    print_commands()
else:
    commands[sys.argv[1]]()
