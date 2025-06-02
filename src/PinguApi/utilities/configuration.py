from django.core.exceptions import ValidationError


def verify_config(config_data: dict, default_config):
    # Define a set of allowed keys from the default configuration
    allowed_keys = set(default_config.keys())
    
    # Check for any extra keys in bot_config_data that are not in allowed_keys
    extra_keys = config_data.keys() - allowed_keys
    if extra_keys:
        raise ValidationError({"error": f"Invalid keys found: {', '.join(extra_keys)}"})
    
    # Verify each key's value against its expected type in the default configuration
    for key, value in default_config.items():
        if key in config_data:
            actual_value = config_data[key]
            if value is None:  # No validation needed for keys with no restrictions on their values
                continue
            if not isinstance(actual_value, type(value)):
                raise ValidationError({f"error": f"Key '{key}' is of type {type(actual_value).__name__}, expected {type(value).__name__}"})


def replace_test_prefix(data, new_prefix: str):
    def recursive_replace(d):
        if isinstance(d, dict):
            return {k: recursive_replace(v) for k, v in d.items()}
        elif isinstance(d, str) and d.startswith('test-'):
            return new_prefix.lower() + d[len('test-'):]
        else:
            return d

    return recursive_replace(data)

def get_bigquery_bucket(config):
    return config['bigquery']['bucket']

def get_coverage_bucket(config):
    return config['coverage']['bucket']
    
def get_all_buckets(config):
    """
    Recursively fetch all bucket values from a nested dictionary.
    
    Args:
        config (dict): The parsed YAML content using yaml.safe_load.

    Returns:
        list: A list of all bucket values in the YAML data.
    """
    buckets = []

    def recursive_search(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'bucket' and isinstance(value, str):
                    buckets.append(value.lower())
                else:
                    recursive_search(value)
        elif isinstance(data, list):
            for item in data:
                recursive_search(item)

    recursive_search(config)
    return buckets

def get_value(config, key_path: str):
    try:
        keys = key_path.split('.')
        for key in keys:
            config = config[key]
        return config
    except (KeyError, TypeError):
        return None
    
def get_build_bucket_by_type(build_type, configuration):
    bucket_name = ""
    match build_type:
        case 'Release':
            bucket_name = get_value(config=configuration, key_path="build.release.bucket")
        case 'SYM_Release':
            bucket_name = get_value(config=configuration, key_path="build.sym-release.bucket")
        case 'SYM_Debug':
            bucket_name = get_value(config=configuration, key_path="build.sym-debug.bucket")
        case 'Stable':
            bucket_name = get_value(config=configuration, key_path="build.stable-build.bucket")
        case 'Beta':
            bucket_name = get_value(config=configuration, key_path="build.beta-build.bucket")
        case _:
            bucket_name = get_value(config=configuration, key_path="build.release.bucket")
    return bucket_name