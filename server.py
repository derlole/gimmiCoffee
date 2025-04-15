
from flask import Flask
from routes.unsecure_routes import unsecure

app = Flask(__name__, static_url_path='/unsecure/static')

# Blueprint registrieren
app.register_blueprint(unsecure)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3060)
