#!/bin/bash

spark/bin/spark-submit \
	--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.2.2 \
	./scripts/consumer/moving_average.py
