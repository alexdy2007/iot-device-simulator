# Databricks notebook source
import os
import requests
import numpy as np
import pandas as pd
import json

token = ''''''

def create_tf_serving_json(data):
    return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

def score_model(dataset):
    url = 'https://45c4a055291f4b5c9534691b42fef03a.serving.cloud.databricks.com/1444828305810485/serving-endpoints/Device_Flow/invocations'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    ds_dict = {'dataframe_split': dataset.to_dict(orient='split')} if isinstance(dataset, pd.DataFrame) else create_tf_serving_json(dataset)
    data_json = json.dumps(ds_dict, allow_nan=True)
    response = requests.request(method='POST', headers=headers, url=url, data=data_json)
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()

# COMMAND ----------

dataset.to_dict(orient='split')

# COMMAND ----------

import pandas as pd

dataset = pd.DataFrame({
  "attribute":["voltage".''],
  "value":[10.22731601]
})

score_model(dataset)

# COMMAND ----------

a = os.environ.get("DATABRICKS_OAUTH_TOKEN")
a

# COMMAND ----------


