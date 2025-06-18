import boto3
from datetime import datetime, timezone, timedelta

# Set retention period
RETENTION_MINUTES = 30
bucket_name = 's3-cleanup-assignment-sainath'


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    now = datetime.now(timezone.utc)
    deleted_files = []

    response = s3.list_objects_v2(Bucket=bucket_name)
    for obj in response.get('Contents', []):
        key = obj['Key']
        last_modified = obj['LastModified']
        age = now - last_modified

        if age > timedelta(minutes=RETENTION_MINUTES):
            print(f"Deleting: {key} (LastModified: {last_modified})")
            s3.delete_object(Bucket=bucket_name, Key=key)
            deleted_files.append(key)

    if not deleted_files:
        print("No files were deleted.")
    else:
        print(f"Deleted {len(deleted_files)} file(s): {deleted_files}")
