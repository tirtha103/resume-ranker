from flask import Flask, render_template, request, send_file
import os
from rank_resumes import rank_resumes
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jd = request.form['jd']
        files = request.files.getlist('resumes')

        # Save uploaded resumes
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        # Rank resumes
        df = rank_resumes(app.config['UPLOAD_FOLDER'], jd)
        df.to_csv("ranked_resumes.csv", index=False)

        return render_template("index.html", tables=[df.to_html(classes='data', index=False)], jd=jd)

    return render_template("index.html", tables=None)

@app.route('/download')
def download():
    return send_file("ranked_resumes.csv", as_attachment=True)

if __name__ == '__main__':
    print("✅ Flask app starting on http://127.0.0.1:5000")
    app.run(debug=True)
