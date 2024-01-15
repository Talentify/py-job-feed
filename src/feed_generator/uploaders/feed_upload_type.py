from enum import Enum


class FeedUploadType(Enum):
    AWS_S3 = 'aws_s3'

    def get_class(self):
        if self == FeedUploadType.AWS_S3:
            from src.feed_generator.uploaders.aws_s3_uploader import AwsS3Uploader
            return AwsS3Uploader
        else:
            raise ValueError(f"invalid feed upload type {self}")
