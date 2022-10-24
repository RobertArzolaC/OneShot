from flask import (
    Blueprint, render_template, current_app, request, 
    redirect, url_for
)
from flask_login import login_required, current_user

from src.services import OneShot


main = Blueprint('main', __name__)
UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']


@main.route('/signed-documents', methods=["GET", "POST"])
@login_required
def signed_documents():
    error = None
    if request.method == "POST":
        given_name = request.form.get("given_name")
        surname_1 = request.form.get("surname_1")
        surname_2 = request.form.get("surname_2")
        id_document = request.form.get("id_document")
        email = request.form.get("email")
        upload_data = request.files.get("document_pdf")
        mobile_phone_number = request.form.get("mobile_phone_number")

        service = OneShot()
        service.build_payload(
            given_name,
            surname_1,
            surname_2,
            email,
            id_document,
            mobile_phone_number,
            current_user.alias,
            current_user.token,
        )
        data_json = service.send_data()
        if data_json:
            code = data_json["details"]
            service.generate_otp(code)
            response = service.upload_file(code, upload_data)
            if "200" in response["status"]:
                document_id = response["details"]
                return redirect(
                    url_for(
                        "main.add_otp",
                        code=code,
                        document_id=document_id,
                    )
                )

        error = "No se pudo enviar la información."

    return render_template('signed-documents.html', error=error)


@main.route('/add-otp/<code>/<document_id>', methods=["GET", "POST"])
@login_required
def add_otp(code, document_id):
    if request.method == "POST":
        otp = request.form.get("otp_code")
        service = OneShot()
        service.build_payload_otp(otp, document_id)
        result = service.send_otp(code)
        if result and "200" in result["status"]:
            return redirect(
                url_for(
                    "main.download_signed_file",
                    code=code,
                    document_id=document_id,
                )
            )

    return render_template('add-otp.html')


@main.route('/download-signed-file/<code>/<document_id>')
@login_required
def download_signed_file(code, document_id):
    service = OneShot()
    url_dowload_file = service.get_download_file_url(
        code, document_id
    )
    return render_template(
        "download_signed_file.html", file_link=url_dowload_file
    )