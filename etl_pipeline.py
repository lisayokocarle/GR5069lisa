# Databricks notebook source
# MAGIC %md ### Import functions

# COMMAND ----------

from pyspark.sql.functions import datediff, current_date, avg
from pyspark.sql.types import IntegerType


# COMMAND ----------

# MAGIC %md ### Read in Dataset 

# COMMAND ----------

df_laptimes = spark.read.csv('s3://columbia-gr5069-main/raw/lap_times.csv', header = True)

# COMMAND ----------

display(df_laptimes)

# COMMAND ----------

df_drivers = spark.read.csv('s3://columbia-gr5069-main/raw/drivers.csv', header = True)

# COMMAND ----------

display(df_drivers)

# COMMAND ----------

# MAGIC %md ### Transform Data

# COMMAND ----------

df_drivers = df_drivers.withColumn('age', datediff(current_date(), df_drivers.dob)/365)

# COMMAND ----------

df_drivers = df_drivers.withColumn('age', df_drivers['age'].cast(IntegerType()))

# COMMAND ----------

df_lap_drivers = df_drivers.select('driverRef', 'code', 'forename', 'surname', 'nationality', 'age', 'driverId').join(df_laptimes, on = ['driverId'])

# COMMAND ----------

display(df_lap_drivers)

# COMMAND ----------

df_races = spark.read.csv('s3://columbia-gr5069-main/raw/races.csv', header = True)

# COMMAND ----------

display(df_races)

# COMMAND ----------

df_lap_drivers = df_lap_drivers.join(df_races.select('year', 'name', 'raceId'), on=["raceId"])

# COMMAND ----------

df_driver_laps = df_lap_drivers.drop('driverId', 'raceId')

# COMMAND ----------

display(df_lap_drivers)

# COMMAND ----------

display(df_driver_laps)

# COMMAND ----------

# MAGIC %md ### Aggregate by Age

# COMMAND ----------

df_agg_age = df_driver_laps.groupby('age'). agg(avg('milliseconds'))

# COMMAND ----------

display(df_agg_age)

# COMMAND ----------

# MAGIC %md ### Storing Data in S3

# COMMAND ----------

df_agg_age.write.csv('s3://lyc2121-gr5069/processed/inclass/laptimes_by_age')

# COMMAND ----------


