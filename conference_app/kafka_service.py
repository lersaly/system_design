from kafka import KafkaConsumer, KafkaProducer
import json
import asyncpg

class KafkaService:
    def __init__(self, bootstrap_servers=['kafka:9092'], topic='talks_topic'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='talks-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    
    def publish_talk_creation(self, talk_data):
        """Публикация сообщения о создании доклада"""
        self.producer.send(self.topic, talk_data)
        self.producer.flush()
    
    async def consume_talks(self):
        """Асинхронный метод потребления сообщений из Kafka"""
        pool = await asyncpg.create_pool(
            user='postgres', 
            password='postgres', 
            database='conference_app', 
            host='db'
        )
        
        for message in self.consumer:
            async with pool.acquire() as connection:
                talk = message.value
                await connection.execute('''
                    INSERT INTO talks (title, description, speaker_id) 
                    VALUES ($1, $2, $3)
                ''', talk['title'], talk.get('description', ''), talk['speaker_id'])