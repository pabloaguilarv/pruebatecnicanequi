import pandas as pd
from datetime import datetime
import boto3

class LoadCSV:
    pass

def lambda_handler(event, context):
    client = boto3.client('s3')

    bucket:str = 'bucket_name'
    path:str = 'pending_path'

    response = client.list_objects_v2(Bucket = bucket)

    