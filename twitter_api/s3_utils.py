import settings

def s3_connection():
    import boto3
    session = boto3.Session()
    credentials = session.get_credentials()
    session = boto3.session.Session(aws_access_key_id=settings.aws_access, aws_secret_access_key=settings.aws_secret)
    return session.resource('s3')

def s3_save(file_path, body, bucket=settings.s3_bucket, s3=s3_connection()):
    object=s3.Object(bucket,file_path)
    object.put(Body=body)
