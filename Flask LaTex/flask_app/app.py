from flask import Flask, render_template, request, send_file
from pylatexenc.latex2text import LatexNodes2Text
from docx import Document
from docx.shared import Inches
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    latex_text = request.form['latex']
    converter = LatexNodes2Text()
    plain_text = converter.latex_to_text(latex_text)
    bullet_points = plain_text.split('\n')

    return {'bullet_points': bullet_points}

@app.route('/export', methods=['POST'])
def export():
    bullet_points = request.form.getlist('bullet_points[]')
    document = Document()

    # Set narrow margins (0.5 inches)
    sections = document.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    for point in bullet_points:
        document.add_paragraph(point, style='ListBullet')

    docx_stream = BytesIO()
    document.save(docx_stream)
    docx_stream.seek(0)

    return send_file(docx_stream, as_attachment=True, download_name='bullet_points.docx')

if __name__ == '__main__':
    app.run(debug=True)