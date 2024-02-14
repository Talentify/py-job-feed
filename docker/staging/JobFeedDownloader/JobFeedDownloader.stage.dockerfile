FROM 124082513016.dkr.ecr.us-east-1.amazonaws.com/py-job-feed-core:stage

COPY ./src/feed_downloader .

RUN python -m setup sdist && \
    pip install dist/*.tar.gz

COPY ./docker/staging/JobFeedDownloader/gunicorn_config.py /app/gunicorn_config.py

CMD ["gunicorn", "--config", "/app/gunicorn_config.py", "app:app"]
