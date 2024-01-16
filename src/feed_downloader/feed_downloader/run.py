from feed_downloader import create_app
from settings import APP_HOST, APP_PORT, DEBUG

app = create_app()

if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=DEBUG)
    