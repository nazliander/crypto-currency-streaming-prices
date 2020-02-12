from flask import Response, Flask
import json
from kafka import KafkaConsumer

application = Flask(__name__)


@application.route('/crypto_latest_trends/')
def kafkaStream():
    consumer_processed = KafkaConsumer(
                    bootstrap_servers="http://kafka:29092",
                    auto_offset_reset="latest",
                    value_deserializer=lambda m: json.loads(m.decode("ascii")))

    consumer_processed.subscribe(topics=["crypto_latest_trends"])

    def crypto_latest_trends():
        result = []
        for message in consumer_processed:
            if message is not None:
                result.append(str(message.value))
            yield result

    return Response(crypto_latest_trends())


if __name__ == '__main__':
    application.run(debug=True)
