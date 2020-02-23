# Spark Structured Streaming Project for Cryptocurrency Prices

A Python project for analysing real-time crypto-currency prices using Kafka and Spark Structured Streaming.

To run the producer and kafka services:

`docker-compose up`

To run the consumer from spark-master:

`docker exec spark-master bash scripts/start_consumer.sh`

## Producer

* Cryptocurrency data API: Coinranking

* Request: From CryptoAPI Class. Only retrieves the analysis attributes.

```
{"nameCoin": coin.get("name"),
 "symbolCoin": coin.get("symbol"),
 "numberOfMarkets": coin.get("numberOfMarkets"),
 "volume": coin.get("volume"),
 "marketCap": coin.get("marketCap"),
 "totalSupply": coin.get("totalSupply"),
 "price": coin.get("price"),
 "timestamp_logger": current_milli_time()}
```

* Produces into Kafka topic: `crypto_raw`

## Consumer

* Reads from `crypto_raw`

* Uses Spark Structured Streaming

* Calculates moving average (with window, slide and watermark)

* Other metric ideas (not implemented):
    
    * Relative price change in comparison to Bitcoin
    * Exponential moving average (using Pandas udf)

* Sinking: Console

* Other Sinking ideas (not implemented):

    * Kafka another topic - direct support
    * MongoDB with foreachWriter - requires mongo-client in spark-submit 
    * Object Storage storing - requires aws and hadoop jars in spark-submit and `/spark/jars/` folder
    * Using Flask to show aggregations

## Additional Services

* JMX (Java Management Extensions) Exporter for Prometheus: For Prometheus to consume Java based metrics

* Prometheus: Scraping and storing metrics in a time series db (this is set for Kafka topic monitoring)



