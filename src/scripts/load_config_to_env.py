import os
import yaml
import argparse

def load_config_env(config_path):
    """Load configuration from config.yaml and set environment variables."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Load all 'env' entries into os.environ
    for key, value in config.get("env", {}).items():
        os.environ[key] = str(value)  # Convert all values to strings
        print(f"Set environment variable: {key}={value}")
    
    return config  # Return the full config for further use if needed

def load_config_docker(config_path):
    """Load configuration from config.yaml and print export statements."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Print export statements for all 'env' entries
    for key, value in config.get("env", {}).items():
        value_str = str(value).replace('"', '\\"')  # Escape double quotes
        print(f'export {key}="{value_str}"')
    
    return config

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Load configuration and set environment variables.")
    parser.add_argument("--config", type=str, required=True, help="Path to the config.yaml file")
    args = parser.parse_args()

    # Load the configuration and set environment variables
    load_config_docker(args.config)
