// =====================================
// AI ELIGIBILITY CHECK (LOGIC BASED)
// =====================================

document.getElementById("eligibilityForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const qualification = document.getElementById("qualification").value;
    const percentage = parseFloat(document.getElementById("percentage").value);
    const category = document.getElementById("category").value;

    const resultBox = document.getElementById("result");

    let message = "";
    let eligible = false;

    // -------------------------------
    // ELIGIBILITY RULES (SIMPLE AI)
// -------------------------------

    if (qualification === "10" && percentage >= 35) {
        eligible = true;
    } 
    else if (qualification === "12" && percentage >= 40) {
        eligible = true;
    } 
    else if (qualification === "iti" && percentage >= 50) {
        eligible = true;
    }

    // -------------------------------
    // CATEGORY BONUS (SIMULATION)
    // -------------------------------
    if (eligible && (category === "SC" || category === "ST")) {
        message = "You are eligible for Diploma Admission under Reserved Category.";
    }
    else if (eligible) {
        message = "You are eligible for Diploma Admission.";
    }
    else {
        message = "You are NOT eligible for Diploma Admission.";
    }

    // -------------------------------
    // DISPLAY RESULT
    // -------------------------------
    resultBox.classList.remove("d-none");
    resultBox.innerHTML = message;

    if (eligible) {
        resultBox.className = "alert alert-success mt-4 text-center";
    } else {
        resultBox.className = "alert alert-danger mt-4 text-center";
    }
});