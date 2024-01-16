from flask import jsonify, Blueprint, Response

from feed_downloader.services.aws import get_aws_s3_client
from feed_downloader.settings import AWS_BUCKET, FEED_DOWNLOAD_CHUNK_SIZE

feed_bp = Blueprint('feed', __name__)


@feed_bp.route('/<token>/', methods=['GET'])
def list_files(token):
    s3 = get_aws_s3_client()

    try:
        response = s3.list_objects_v2(Bucket=AWS_BUCKET, Prefix=token)

        files = [obj['Key'] for obj in response.get('Contents', [])]

        return jsonify({'files': files})

    except Exception as e:
        return str(e)


@feed_bp.route('/<token>/<page>', methods=['GET'])
def download_file(token, page):
    s3 = get_aws_s3_client()

    s3_key = f"{token}/feed_{page}.xml"

    response = s3.get_object(Bucket=AWS_BUCKET, Key=s3_key)

    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': f'attachment; filename={s3_key.split("/")[-1]}',
        'Content-Length': response['ContentLength']
    }

    return Response(
        response['Body'].iter_chunks(chunk_size=FEED_DOWNLOAD_CHUNK_SIZE),
        headers=headers,
        status=200
    )
