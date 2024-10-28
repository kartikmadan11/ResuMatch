import boto3


def fetch_all_keys_from_s3(
    s3_bucket, aws_access_key_id, aws_secret_access_key, aws_default_region
):
    print(f"Fetching all keys from S3 bucket initiated")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_default_region,
    )

    s3 = session.client("s3")
    objects = s3.list_objects_v2(Bucket=s3_bucket)

    all_keys = [obj["Key"] for obj in objects.get("Contents", [])]
    print(f"Total keys fetched: {len(all_keys)}")
    return all_keys
