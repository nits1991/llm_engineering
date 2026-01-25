"""
S3 Uploader Module
==================

Upload generated content to AWS S3 bucket.
Requires AWS credentials to be configured.
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
from datetime import datetime


def upload_to_s3(content: str, bucket_name: str, file_key: str, content_type: str = 'text/markdown') -> str:
    """
    Upload content to AWS S3 bucket.

    Args:
        content: Content to upload (string or bytes)
        bucket_name: S3 bucket name
        file_key: S3 object key (path + filename)
        content_type: MIME type of content

    Returns:
        S3 URL of uploaded file

    Raises:
        Exception: If upload fails
    """

    # Initialize S3 client
    # Uses credentials from ~/.aws/credentials or environment variables
    try:
        s3_client = boto3.client('s3')
    except NoCredentialsError:
        raise Exception(
            "AWS credentials not found. "
            "Please configure AWS credentials using:\n"
            "  - AWS CLI: aws configure\n"
            "  - Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY\n"
            "  - ~/.aws/credentials file"
        )

    # Convert content to bytes if it's a string
    if isinstance(content, str):
        content_bytes = content.encode('utf-8')
    else:
        content_bytes = content

    # Upload to S3
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=content_bytes,
            ContentType=content_type,
            Metadata={
                'uploaded_at': datetime.now().isoformat(),
                'uploaded_by': 'AI Content Generator'
            }
        )

        # Generate S3 URL
        s3_url = f"s3://{bucket_name}/{file_key}"

        # Also generate HTTPS URL if bucket is public
        https_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"

        return https_url

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            raise Exception(f"S3 bucket '{bucket_name}' does not exist")
        elif error_code == 'AccessDenied':
            raise Exception(
                f"Access denied to S3 bucket '{bucket_name}'. Check your AWS permissions.")
        else:
            raise Exception(f"Failed to upload to S3: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error uploading to S3: {str(e)}")


def upload_pdf_to_s3(pdf_bytes: bytes, bucket_name: str, file_key: str) -> str:
    """
    Upload PDF file to S3.

    Args:
        pdf_bytes: PDF content as bytes
        bucket_name: S3 bucket name
        file_key: S3 object key

    Returns:
        S3 URL of uploaded file
    """
    return upload_to_s3(pdf_bytes, bucket_name, file_key, content_type='application/pdf')


def list_s3_objects(bucket_name: str, prefix: str = '') -> list:
    """
    List objects in S3 bucket.

    Args:
        bucket_name: S3 bucket name
        prefix: Filter objects by prefix

    Returns:
        List of object keys
    """
    try:
        s3_client = boto3.client('s3')
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        return []

    except ClientError as e:
        raise Exception(f"Failed to list S3 objects: {str(e)}")


def check_s3_access(bucket_name: str) -> bool:
    """
    Check if we have access to S3 bucket.

    Args:
        bucket_name: S3 bucket name

    Returns:
        True if accessible, False otherwise
    """
    try:
        s3_client = boto3.client('s3')
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except:
        return False


def create_s3_bucket(bucket_name: str, region: str = 'us-east-1') -> bool:
    """
    Create a new S3 bucket.

    Args:
        bucket_name: Name for the new bucket
        region: AWS region

    Returns:
        True if successful, False otherwise
    """
    try:
        s3_client = boto3.client('s3', region_name=region)

        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        return True

    except ClientError as e:
        raise Exception(f"Failed to create S3 bucket: {str(e)}")
