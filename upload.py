import os
from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath('.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML = """
<!doctype html>
<title>Upload e Listagem</title>
<h1>Upload de Arquivo</h1>
<form method=post enctype=multipart/form-data action="{{ url_for('upload') }}">
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
<h2>Arquivos na Pasta Atual</h2>
<ul>
{% for f in files %}
  <li>
    {{ f }}
    [<a href="{{ url_for('download', filename=f) }}">download</a>]
  </li>
{% endfor %}
</ul>
"""

@app.route('/')
def index():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER'])
             if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return render_template_string(HTML, files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # Permitir conexões de qualquer IP
    app.run(host='0.0.0.0', debug=True)
