FROM 124082513016.dkr.ecr.us-east-1.amazonaws.com/py-job-feed-core:stage

COPY ./src/feed_generator .

RUN python -m setup sdist && \
    pip install dist/*.tar.gz
