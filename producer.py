from kafka import KafkaProducer
import json
producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('Ian_Tristan_Server.public.customers', {'first_name': 'Alice', 'last_name': 'Smith'})
producer.flush()
