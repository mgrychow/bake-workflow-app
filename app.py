from flask import Flask

def get_app():
    app = Flask(__name__)

    @app.route('/ping')
    def ping():
        return "pong\n"

    return app

def main():
    app = get_app()
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()