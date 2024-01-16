import boto3
from flask import send_file, jsonify, Blueprint, Response

from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET

feed_bp = Blueprint('feed', __name__)


@feed_bp.route('/<token>/', methods=['GET'])
def list_files(token):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        # List objects in the specified S3 bucket and prefix
        response = s3.list_objects_v2(Bucket=AWS_BUCKET, Prefix=token)

        # Extract the file names from the response
        files = [obj['Key'] for obj in response.get('Contents', [])]

        return jsonify({'files': files})

    except Exception as e:
        return str(e)


@feed_bp.route('/<token>/<page>', methods=['GET'])
def download_file(token, page):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    s3_key = f"{token}/feed_{page}.xml"

    response = s3.get_object(Bucket=AWS_BUCKET, Key=s3_key)

    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': f'attachment; filename={s3_key.split("/")[-1]}',
        'Content-Length': response['ContentLength']
    }

    return Response(
        response['Body'].iter_chunks(chunk_size=1024),
        headers=headers,
        status=200
    )
