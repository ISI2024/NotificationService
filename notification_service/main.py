import logging
from queue_manager import KafkaConsumerActor

def setup_logging():
    fileHandler = logging.FileHandler("{0}/{1}.log".format("./logs", "notification_service"))
    console_handler = logging.StreamHandler()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", handlers=[fileHandler, console_handler])


if __name__ == "__main__":
    setup_logging()
    logging.info("Application started")
    actor = KafkaConsumerActor.start().proxy().on_receive()