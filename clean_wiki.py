import sys
from pyspark.sql import SparkSession


def process_file(filepath):
    spark = (
        SparkSession.builder.master("local")
        .appName("Colab")
        .config("spark.ui.port", "4050")
        .getOrCreate()
    )

    df = spark.read.csv(filepath, header=True)
    df.createOrReplaceTempView("wiki")
    df.printSchema()

    spark.sql("SELECT * FROM wiki LIMIT 5;").show(5, 0)

    regex1, replace1 = r"-LRB-", "("
    regex2, replace2 = r"-RRB-", ")"
    regex3, replace3 = r"\'\' *", ""
    regex4, replace4 = r", ; *", ""
    regex5, replace5 = r"; , *", ""
    regex6, replace6 = r", , *", ""
    regex7, replace7 = r"; ; *", ""
    regex8, replace8 = r"[(] [;,-]* [)] ", ""
    regex9, replace9 = r"[(] +[)] *", ""

    iterable = (
        (regex1, replace1),
        (regex2, replace2),
        (regex3, replace3),
        (regex4, replace4),
        (regex5, replace5),
        (regex6, replace6),
        (regex7, replace7),
        (regex8, replace8),
        (regex9, replace9),
    )

    for regex, replace in iterable:
        query = f"SELECT \
        regexp_replace(original_text, '{regex}', '{replace}') as original_text, \
        label FROM wiki;"

    df = spark.sql(query)
    df.createOrReplaceTempView("wiki")

    query = r"SELECT * FROM wiki WHERE LENGTH(original_text) > 20;"
    df = spark.sql(query)
    df.createOrReplaceTempView("wiki")

    df.show(5, 0)

    return df.toPandas()
