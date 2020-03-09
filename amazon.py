from io import StringIO
import logging
import boto3
from botocore.exceptions import ClientError
import pandas as pd
from DEFAULTS import REGION_NAME, S3_BUCKET
from helpers.utils import log_exception

logger = logging.getLogger(__name__)

def get_aws_service(service_name, region_name=REGION_NAME):
    return boto3.client(service_name,
                        region_name=region_name)

def read_file_from_s3(file_name, bucket=S3_BUCKET, region_name = REGION_NAME):
    try:
        client = get_aws_service(service_name="s3", region_name = region_name)
        logger.info(f"Getting file {file_name} from S3: bucket: {bucket} region: {region_name}")
        csv_obj = client.get_object(Bucket=bucket, Key=file_name)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))
        return df
    except ClientError as ce:
        log_exception()