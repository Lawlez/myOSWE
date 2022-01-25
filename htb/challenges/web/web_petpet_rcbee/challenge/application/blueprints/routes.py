from flask import Blueprint, request, render_template
from application.util import petpet

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@api.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return {'status': 'failed', 'message': 'No file provided'}, 400

    file = request.files['file']

    if not file or not file.filename:
        return {'status': 'failed', 'message': 'Something went wrong with the file'}, 400

    return petpet(file)