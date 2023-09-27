from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='xxx:9092')
producer.send("lfsdk_message_import",b'test send kafka message by zxx1')
producer.flush()
