import os
import yaml
from scripts.load_config_to_env import load_config_env


# load backend component configuration into enviroment context
load_config_env("config/system/config.yaml")
load_config_env("config/redis/config.yaml")
load_config_env("config/database/config.yaml")
load_config_env("config/minio/config.yaml")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PinguBackend.settings.development")
import django
django.setup()

from django.contrib.auth.models import User

def load_config():
    """Load configuration from config.yaml."""
    with open("config/system/config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

def create_admin_user(config):
    """Create a Django admin user."""
    username = config["admin"]["username"]
    email = config["admin"]["email"]
    password = config["admin"]["password"]

    if User.objects.filter(username=username).exists():
        print(f"Admin user '{username}' already exists.")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Admin user '{username}' created.")

if __name__ == "__main__":
    config = load_config()
    create_admin_user(config)
