// ==================================================
// CAPITAL LETTER + SPACE CLEANING
// ==================================================
document.querySelectorAll(
    "input[type='text'], textarea"
).forEach(field => {
    field.addEventListener("input", () => {
        field.value = field.value
            .toUpperCase()
            .replace(/\s+/g, " ")
            .trim();
    });
});

// ==================================================
// PHONE NUMBER VALIDATION (10 DIGITS)
// ==================================================
function onlyNumbers(input) {
    input.value = input.value.replace(/\D/g, "");

    if (input.value.length > 10) {
        input.value = input.value.slice(0, 10);
    }
}

document.querySelectorAll(
    "input[name='parent_phone1'], input[name='parent_phone2'], input[name='student_phone']"
).forEach(phone => {
    phone.addEventListener("input", () => onlyNumbers(phone));
});

// ==================================================
// EMAIL BASIC VALIDATION
// ==================================================
const emailField = document.querySelector("input[name='student_email']");
if (emailField) {
    emailField.addEventListener("blur", function () {
        if (this.value && !this.value.includes("@")) {
            alert("Please enter a valid Email ID");
            this.focus();
        }
    });
}

// ==================================================
// COPY RESIDENTIAL ADDRESS → PERMANENT ADDRESS
// ==================================================
function copyAddress(checkbox) {
    const res = document.getElementById("res_address");
    const perm = document.getElementById("perm_address");

    if (checkbox.checked) {
        perm.value = res.value;
        perm.readOnly = true;
    } else {
        perm.value = "";
        perm.readOnly = false;
    }
}

// ==================================================
// FORM VALIDATION BEFORE SUBMIT
// ==================================================
document.querySelector("form").addEventListener("submit", function (e) {

    const parentPhone = document.querySelector("input[name='parent_phone1']").value;
    const studentPhone = document.querySelector("input[name='student_phone']").value;

    if (parentPhone.length !== 10) {
        alert("Parent phone number must be exactly 10 digits");
        e.preventDefault();
        return;
    }

    if (studentPhone.length !== 10) {
        alert("Student phone number must be exactly 10 digits");
        e.preventDefault();
        return;
    }
});