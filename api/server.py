import config

connex_app = config.connex_app
connex_app.add_api('swagger.yaml')

if __name__ == '__main__':
    connex_app.run(port=5000, debug=connex_app.app.config['DEBUG'])
