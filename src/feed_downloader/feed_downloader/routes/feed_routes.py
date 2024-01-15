import boto3
from flask import send_file, jsonify, Blueprint

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

    try:
        filename = f"feed_{page}.xml"
        # Download the file from S3
        s3.download_file(AWS_BUCKET, f"{token}/{filename}", filename)

        # Send the downloaded file to the client
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e)