import yaml
from pydantic import BaseModel

class Gmail(BaseModel):
    address: str
    password: str
    server: str
    port: int

class Config:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config = {}
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            with open("config.yaml", "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)

                self.kafka_config = {
                    'bootstrap.servers': config['kafka']['host'],
                    'group.id': 'notifications',
                    'auto.offset.reset': 'earliest',
                    'enable.auto.commit': False,
                    'security.protocol': 'SASL_PLAINTEXT',
                    'sasl.mechanisms': 'PLAIN',
                    'sasl.username': config['kafka']['user'],
                    'sasl.password': config['kafka']['password']
                }
                
                self.topics = config['kafka']['topics']

                self.email = Gmail(address=config['email']['sender'],
                                   password=config['email']['sender_password'],
                                   server=config['email']['sever'],
                                   port=config['email']['port'])
                self.templates_dir = config["templates_dir"]