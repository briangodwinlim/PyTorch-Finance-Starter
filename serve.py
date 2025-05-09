import json
import mlflow
import numpy as np
import datetime as dt
from pipeline.data import StockDataset
from sklearn.preprocessing import StandardScaler
from mlflow.models.flavor_backend_registry import get_flavor_backend

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# [MLFlow] Inference set-up
tracking_uri = 'http://127.0.0.1:8080'
mlflow.set_tracking_uri(uri=tracking_uri)
model_uri = 'runs:/123456789/model'     # 'models:/TimeSeriesModel/1'   (After registering the model)

# Server options
env_manager = 'uv'
enable_mlserver = False
model_api_port = 4001
model_api_host = 'localhost'
timeout = 60


# Sample input data
train_dataset = StockDataset(dt.datetime(2018,1,1), dt.datetime(2020,12,31), 10, 
                             transform_spec={'features': StandardScaler(), 'targets': StandardScaler(), 
                                             'features_fit': True, 'targets_fit': True})
input_data, _ = train_dataset[0]
input_data = np.expand_dims(input_data.numpy(), axis=0)


# Option 1: Python programmatic approach
mlflow.models.predict(
    model_uri=model_uri,
    input_data=input_data,
    env_manager=env_manager,
)


# Option 2: Set-up an API for the model
# payload = json.dumps({"inputs": input_data.tolist()})
# print('Run the following command on the terminal: \n')
# print(f'curl localhost:{model_api_port}/invocations -H "Content-Type: application/json" --data \'{payload}\' \n')
# get_flavor_backend(model_uri, docker_build=True, env_manager=env_manager).serve(
#     model_uri=model_uri, 
#     port=model_api_port, 
#     host=model_api_host,
#     timeout=timeout,
#     enable_mlserver=enable_mlserver,
# )
