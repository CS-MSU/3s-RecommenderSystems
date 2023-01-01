import yaml
from waitress import serve
from app import app


with open("project/config.yml", "r") as f:
    config = yaml.load(f, yaml.Loader)


HOST = config.get('server').get('host')
PORT = config.get('server').get('port')


if __name__ == '__main__':
    serve(app, host=HOST, port=PORT)
