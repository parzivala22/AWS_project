from awsglue.utils import getResolvedOptions
import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME", "bucket", "key"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

bucket = args["bucket"]
key = args["key"]

print(f"Reading file from: s3://{bucket}/{key}")

df = spark.read.csv(f"s3://{bucket}/{key}", header=True, inferSchema=True)

output_path = f"s3://{bucket}/output/"

df.write.mode("overwrite").option("header", True).csv(output_path)

df.show()

job.commit()