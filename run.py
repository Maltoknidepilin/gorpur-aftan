import os
import sys

# Patch standard library to cooperate with gevent (https://www.gevent.org/api/gevent.monkey.html)
# Skip patching if run through gunicorn (which does the patching for us)

if len(sys.argv) == 2 and sys.argv[1] == "dev":
    print("Running in dev mode - skipping gevent patching")
elif "gunicorn" not in os.environ.get("SERVER_SOFTWARE", ""):
    from gevent import monkey
    monkey.patch_all()  # Patching needs to be done as early as possible, before other imports

from gevent.pywsgi import WSGIServer

from korp import create_app

if __name__ == "__main__":
    app = create_app()

    if len(sys.argv) == 2 and sys.argv[1] == "dev":
        # Run using Flask (use only for development)
        app.run(debug=True, threaded=True, host=app.config["WSGI_HOST"], port=app.config["WSGI_PORT"])
    else:
        # Run using gevent
        print("Serving using gevent")
        http = WSGIServer((app.config["WSGI_HOST"], app.config["WSGI_PORT"]), app.wsgi_app)
        http.serve_forever()
