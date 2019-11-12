from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


class Source:
    def __init__(self):
        self.conf = SparkConf() \
            .setAppName("Crypto App") \
            .setMaster("spark://spark-master:7077")

        self.sc = SparkContext(conf=self.conf)

        self.spark = SparkSession.builder \
            .config(conf=self.conf) \
            .getOrCreate()
