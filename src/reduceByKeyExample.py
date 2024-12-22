
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("ReduceExample").master("local[*]").getOrCreate()

sc = spark.sparkContext

small_dataset = "/input/dataset.txt"
large_dataset = "/input/large_dataset.txt"
super_large_dataset = "/input/super_large_dataset.txt"

large_skew_dataset = "/input/large_skew_dataset.txt"

lines = sc.textFile(large_skew_dataset)
words = lines.flatMap(lambda line: line.split(" "))
wordPairs = words.map(lambda word: (word, 1))
wordCounts = wordPairs.reduceByKey(lambda acc, count1: acc + count1)


results = wordCounts.collect()
for (word, count1) in results:
    print(f"{word}: {count1}")