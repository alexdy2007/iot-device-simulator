# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION alex_young.device_demo.to_h3(long FLOAT, lat FLOAT, res INT) 
# MAGIC RETURNS BIGINT 
# MAGIC LANGUAGE SQL 
# MAGIC RETURN h3_longlatash3(long, lat, res)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION alex_young.device_demo.to_h3(long FLOAT, lat FLOAT, res INT) 
# MAGIC RETURNS BIGINT 
# MAGIC LANGUAGE PYTHON 
# MAGIC RETURN h3_longlatash3(long, lat, res)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *, alex_young.device_demo.to_h3(longitude, latitude, 10) as h3_lvl_10 FROM alex_young.device_demo.device_enriched

# COMMAND ----------


