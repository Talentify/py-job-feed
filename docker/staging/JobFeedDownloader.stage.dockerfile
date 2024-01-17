FROM 124082513016.dkr.ecr.us-east-1.amazonaws.com/py-job-feed-core:stage

COPY ./src/feed_downloader .

RUN python -m setup sdist && \
    pip install dist/*.tar.gz

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
