from llm_engineering.settings import settings


import boto3, json

client = boto3.client(
            "sagemaker-runtime",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
        )

resp = client.invoke_endpoint(
    EndpointName=settings.SAGEMAKER_ENDPOINT_INFERENCE,
    ContentType="application/json",
    Accept="application/json",
    Body=json.dumps({"inputs": "Can you give me a general information about 3-5-2 tactic in football?"})
)

print(resp["Body"].read())