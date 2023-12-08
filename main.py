import os

from flask import Flask, render_template, request, flash, redirect, send_from_directory, url_for
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename

from image_processing import *

UPLOAD_FOLDER = 'dynamic/user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = "random_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000

filename = ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    global filename
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print('Saving')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File saved')
            print(filename)
            colors = get_color_palette(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(colors)
            return render_template('index.html', image_loaded=filename, colors=colors)
    return render_template('index.html', image_loaded='')


@app.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
    global filename
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/color-palette', methods=['POST', 'GET'])
def color_palette():
    filename = request.args['filename']






if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


