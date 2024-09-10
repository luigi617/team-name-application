from importlib import import_module
from flask import Flask, render_template, Response
import os
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera
    # from test_camera import Camera

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    return app

app = create_app()

# @app.route('/')
# def hello_world():
#     return 'Hello World'
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    
    app.run(debug=app.config["DEBUG"])