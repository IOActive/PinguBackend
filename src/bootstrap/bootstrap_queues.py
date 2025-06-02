import pika
import yaml

def load_config():
    """Load configuration from config.yaml."""
    with open("config/redis/config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

def setup_queues(config):
    """Set up RabbitMQ queues."""
    connection_params = pika.ConnectionParameters(host=config["env"]["QUEUE_HOST"])
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    try:
        for queue in config["queues"]:
            channel.exchange_declare(exchange='src', durable=True)
            channel.queue_declare(queue=queue["name"], durable=True, auto_delete=False)
            channel.queue_bind(exchange='src', queue=queue["name"])
        print("Queues setup complete.")
    except Exception as e:
        print(f"Error setting up queues: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    config = load_config()
    setup_queues(config)
