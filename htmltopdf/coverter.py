from flask import Flask, render_template, make_response, send_from_directory, request, after_this_request
# ------------------ html to pdf ------------------ #
import pdfkit
# ------------------ docx to pdf ------------------ #
import docx2pdf
# ------------------ img to pdf ------------------ #
import img2pdf
from PIL import Image
# ------------------ resume template builder  ------------------ #
from docxtpl import DocxTemplate

# ------------------------------------ #
import os
import pythoncom

app = Flask(__name__)


@app.route("/render/<name>")
def render_page(name):
    return render_template(f'htmltopdf/{name}.html')


@app.route("/docToPdf", methods=['GET', 'POST'])
def doc_to_pdf():
    json_data = request.json
    fileName = (json_data["fileName"]).split(".")[0]
    fileLocation = json_data["filePath"]
    pythoncom.CoInitialize()
    docx2pdf.convert(fileLocation)
    workingdir = os.path.abspath(os.getcwd())
    os.remove(f"{workingdir}/{fileLocation}")
    filepath = workingdir + "/templates/doctopdf/"
    return send_from_directory(filepath, f'{fileName}.pdf', as_attachment=True)


@app.route('/deletefiles')
def delete_f():
    json_data = request.json
    path = json_data["filePath"]
    os.remove(path)


@app.route("/imgtopdf", methods=['GET', 'POST'])
def img_to_pdf():
    json_data = request.json
    img_name = (json_data["fileName"]).split(".")[0]
    file_path = json_data["filePath"]
    working_dir = os.path.abspath(os.getcwd())
    img_path = working_dir + file_path
    pdf_path = working_dir + f"/templates/imgtopdf/{img_name}.pdf"
    image = Image.open(img_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    filepath = working_dir + "/templates/imgtopdf/"
    os.remove(f"{working_dir}/{file_path}")
    return send_from_directory(filepath, f'{img_name}.pdf', as_attachment=True)


@app.route('/tempbuilder')
def temp_builder():
    templateId = "PYTHON OOPS HandsON"
    path = f"templates/doctopdf/{templateId}.docx"
    doc = DocxTemplate(path)
    context = {'company_name': "World company"}
    doc.render(context)
    email = "abc"
    doc.save(f"templates/doctopdf/{email}.docx")
    # doc_to_pdf(filepath)  to be called after completing resume template
    return {
        'fileName': email,
        'filePath': f"/templates/doctopdf/{email}.docx"
    }


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename.split(".")[1] in ["docx"]:
            path = "templates/doctopdf/"
        elif f.filename.split(".")[1] in ["jpg", "jpeg"]:
            path = "templates/imgtopdf/"
        f.save(path + f.filename)
        return {
            'fileName': f.filename,
            'filePath': "/" + path + f.filename
        }


if __name__ == "__main__":
    app.run(debug=True)
