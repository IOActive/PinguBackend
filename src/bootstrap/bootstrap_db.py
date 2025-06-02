import os
import shlex
import subprocess
import yaml

def load_config():
    """Load configuration from config.yaml."""
    with open("config/database/config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

def create_databases(config):
    """Create required databases."""
    databases = config.get("env", {}).get("POSTGRES_DB", [])
    try:
        env = os.environ.copy()
        env["PGPASSWORD"] = config["env"]["POSTGRES_PASSWORD"]  # Set the password in the environment

        for db in databases:
            create_table_sql = f"CREATE DATABASE {db};"
            try:
                psql_command = [
                    'psql',
                    '-h', config["env"]["POSTGRES_HOST"],
                    '-U', config["env"]["POSTGRES_USER"],
                    '-p', str(config["env"]["POSTGRES_PORT"]),
                    '-c', create_table_sql,
                    'postgres'
                ]
                subprocess.run(psql_command, check=True, env=env)
            except subprocess.CalledProcessError as e:
                if 'already exists' in str(e):
                    print(f"Database {db} already exists, skipping.")
                else:
                    print(f"Error creating database {db}: {e}")
                    raise
    finally:
        # Clean the password from the environment
        if "PGPASSWORD" in env:
            del env["PGPASSWORD"]

def apply_migrations():
    """Apply Django migrations."""
    commands = [
        'python manage.py migrate --settings PinguBackend.settings.development',
        'python manage.py makemigrations PinguApi --settings PinguBackend.settings.development',
        'python manage.py migrate PinguApi --database=primary --settings PinguBackend.settings.development',
        'python manage.py migrate PinguApi --database=bigquery --settings PinguBackend.settings.development'
    ]
    for command in commands:
        subprocess.run(shlex.split(command), check=True)

if __name__ == "__main__":
    config = load_config()
    create_databases(config)
    apply_migrations()
