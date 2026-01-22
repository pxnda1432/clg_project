from flask import Flask, render_template, request, redirect, url_for
from database import get_db
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# ===============================
# UPLOAD FOLDERS
# ===============================
PHOTO_FOLDER = "uploads/photos"
CERT_FOLDER = "uploads/certificates"

os.makedirs(PHOTO_FOLDER, exist_ok=True)
os.makedirs(CERT_FOLDER, exist_ok=True)

# ===============================
# ADMISSION ID GENERATOR
# ===============================
def generate_admission_id(branch, year, cursor):
    year_suffix = str(year)[-2:]  # last 2 digits of year

    cursor.execute(
        """
        SELECT admission_id 
        FROM student_admission 
        WHERE branch=%s AND admission_year=%s 
        ORDER BY admission_id DESC 
        LIMIT 1
        """,
        (branch, year)
    )

    last = cursor.fetchone()
    next_num = int(last[0][-3:]) + 1 if last else 1

    return f"{branch}{year_suffix}{str(next_num).zfill(3)}"


# ===============================
# HOME PAGE
# ===============================
@app.route("/")
def home():
    return render_template("index.html")


# ===============================
# ADMISSION FORM
# ===============================
@app.route("/admission", methods=["GET", "POST"])
def admission():
    admission_id = ""

    if request.method == "POST":
        # Convert all text inputs to CAPITAL letters
        data = {k: request.form[k].strip().upper() for k in request.form}

        db = get_db()
        cur = db.cursor()

        # Generate Admission ID
        admission_id = generate_admission_id(
            data["branch"], data["admission_year"], cur
        )

        # ===============================
        # FILE HANDLING
        # ===============================
        photo = request.files.get("student_photo")
        study = request.files.get("study_certificate")
        transfer = request.files.get("transfer_certificate")

        photo_name = secure_filename(photo.filename) if photo and photo.filename else None
        study_name = secure_filename(study.filename)
        transfer_name = secure_filename(transfer.filename)

        if photo_name:
            photo.save(os.path.join(PHOTO_FOLDER, photo_name))

        study.save(os.path.join(CERT_FOLDER, study_name))
        transfer.save(os.path.join(CERT_FOLDER, transfer_name))

        # ===============================
        # DATABASE INSERT (SAFE & CORRECT)
        # ===============================
        cur.execute("""
        INSERT INTO student_admission (
            admission_id,
            admission_year,
            branch,
            first_name,
            middle_name,
            last_name,
            student_photo,
            dob,
            father_name,
            mother_name,
            parent_phone1,
            parent_phone2,
            student_phone,
            student_email,
            residential_address,
            permanent_address,
            aadhar_number,
            income_amount,
            category,
            sub_caste,
            study_certificate,
            transfer_certificate,
            previous_qualification
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s
        )
        """, (
            admission_id,
            data["admission_year"],
            data["branch"],
            data["first_name"],
            data.get("middle_name"),
            data.get("last_name"),
            photo_name,
            data["dob"],
            data["father_name"],
            data["mother_name"],
            data["parent_phone1"],
            data.get("parent_phone2"),
            data["student_phone"],
            data.get("student_email"),
            data.get("residential_address"),
            data.get("permanent_address"),
            data.get("aadhar_number"),
            data.get("income_amount"),
            data.get("category"),
            data.get("sub_caste"),
            study_name,
            transfer_name,
            data["previous_qualification"]
        ))

        db.commit()

        # After submit → show form again with generated Admission ID
        return render_template("admission.html", admission_id=admission_id)

    # GET request
    return render_template("admission.html", admission_id=admission_id)


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
