from flask import Flask, render_template, make_response, send_from_directory, request, after_this_request
# ------------------ html to pdf ------------------ #
import pdfkit
# ------------------ docx to pdf ------------------ #
import docx2pdf
# ------------------ img to pdf ------------------ #
import img2pdf
from PIL import Image

# ------------------------------------ #
import os
import pythoncom


app = Flask(__name__)


@app.route("/render/<name>")
def render_page(name):
    return render_template(f'htmltopdf/{name}.html')


@app.route("/htmltopdf/<name>")
def html_to_pdf(name):
    path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdf = pdfkit.from_url("http://127.0.0.1:5000/render/index", False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename={name}.pdf"
    return response


def remover(function):
    def wrapper():
        function()
    return wrapper


@remover
@app.route("/docToPdf/mohit", methods=['GET', 'POST'])
def doc_to_pdf():
    pythoncom.CoInitialize()
    docx2pdf.convert("templates/doctopdf/PYTHON OOPS HandsON.docx")
    # os.remove(f"{workingdir}/templates/imgtopdf/{img_path}")
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + "/templates/doctopdf/"
    return send_from_directory(filepath, 'PYTHON OOPS HandsON.pdf', as_attachment=True)


def delete_file(path):
    for i in path:
        os.remove(path)


@app.route("/imgtopdf/<name>")
def img_to_pdf(name):
    img_name = "download.jpg"
    workingdir = os.path.abspath(os.getcwd())
    img_path = workingdir + f"/templates/imgtopdf/{img_name}"
    # os.remove(f"{workingdir}/templates/imgtopdf/{img_path}")
    pdf_path = workingdir + f"/templates/imgtopdf/result.pdf"
    image = Image.open(img_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    filepath = workingdir + "/templates/imgtopdf/"
    return send_from_directory(filepath, 'result.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
