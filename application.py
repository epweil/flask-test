import flask
import os
 
application = flask.Flask(__name__)

@application.route('/')
def hello_world():
    message = "Hello, world!"
    return flask.render_template('planes.html')
 
if __name__ == '__main__':'
    app.config['planes'] = []
    application.run(host='0.0.0.0')
