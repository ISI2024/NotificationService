import pykka
from confluent_kafka import Consumer, KafkaError, KafkaException
from config import Config
from email_actor import EmailSenderActor
from schemas import Templates, EmailActorMessage, UsersEvent, UsersEventType, TestsEvent, TestsEventType
from logging import log, INFO, ERROR, DEBUG
import json


config = Config()

kafka_conf_consumer = {
    'bootstrap.servers': config.kafka_host,
    'group.id': 'notifications',
    'auto.offset.reset': 'latest'
}

class KafkaConsumerActor(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        self.consumer = Consumer(kafka_conf_consumer)
        self.topics = config.topics
        self.email_actor = EmailSenderActor.start()
        self.running = True

    def on_receive(self):
        self.consumer.subscribe(self.topics)  

        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        log(ERROR, msg.error())
                        raise KafkaException(msg.error())

                if msg.topic() == "users":
                    self.on_users_message(message=msg.value().decode("utf-8"))
                else:
                    self.on_tests_message(message=msg.value().decode("utf-8"))

        except Exception as e:
            log(ERROR, f'Error during event consumption: {e}')

    def on_stop(self):
        self.running = False
        self.consumer.close()
        self.email_actor.stop()

    
    def on_users_message(self, message: str):
        try:
            message_json = json.loads(message)
            decoded = UsersEvent(**message_json)

            match decoded.kind:
                case UsersEventType.NEW_VERIFICATION:
                    log(INFO, f"Consumed user new verification event: {decoded.data}")
                    self.email_actor.tell(EmailActorMessage(recipient=decoded.data.email, template=Templates.VERIFICATION_CODE, context={'code': decoded.data.code}))
                case _:
                    log(DEBUG, f"Unsupported users command: {decoded.kind}")
               

        except Exception as e:
            log(ERROR, f"Unable to process user event message: {e}")

    def on_tests_message(self, message: str):
        try:
            message = json.loads(message)
            decoded = TestsEvent(**message)

            match decoded.kind:
                case TestsEventType.FINISHED_TEST:
                    log(INFO, f"Consumed test finish event: {decoded.data}")
                    self.email_actor.tell(EmailActorMessage(recipient=decoded.data.email, template=Templates.FINISHED_TEST))
                case _:
                    log(DEBUG, f"Unsupported tests command: {decoded.kind}")

            
        except Exception as e:
            log(ERROR, f"Unable to process tests event message: {e}")  

# {"kind": "FINISHED_TEST","data": {"email": "adam.naworski2000@gmail.com", "result": null}}
# {"kind": "NEW_VERIFICATION","data": {"code":"111111","email":"adam.naworski2000@gmail.com"}}     