
const form = document.getElementById("loanForm");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("customerName").value.trim();
    const amount = Number(document.getElementById("loanAmount").value);
    const loanType = document.getElementById("loanType").value;
    const pan = document.getElementById("panNumber").value.trim().toUpperCase();
    const phone = document.getElementById("phone").value.trim();
    const email = document.getElementById("email").value.trim();

    if (name === "" || amount <= 0 || loanType === "" || pan === "" || phone === "" || email === "") {
        alert("Please fill all fields correctly!");
        return;
    }


    if (!/^[A-Z]{5}[0-9]{4}[A-Z]$/.test(pan)) {
        alert("Please enter a valid PAN format!");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/applications", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                customer_name: name,
                phone: phone,
                email: email,
                loan_amount: amount,
                loan_type: loanType,
                pan_number: pan

            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Application submission failed");
        }

        alert(
            "Application submitted successfully!\nApplication ID: " +
            result.application_id
        );

        form.reset();

    } catch (error) {
        alert("Error: " + error.message);
        console.error(error);
    }
});

// This Function calculates EMI


const loanAmountInput = document.getElementById("loanAmount");
const interestRateInput = document.getElementById("interestRate");
const loanTenureInput = document.getElementById("loanTenure");
const emiResult = document.getElementById("emiResult");

function calculateEMI() {
    const principal = Number(loanAmountInput.value);
    const annualRate = Number(interestRateInput.value);
    const years = Number(loanTenureInput.value);

    if (principal <= 0 || annualRate <= 0 || years <= 0) {
        emiResult.textContent = "Monthly EMI: ₹0";
        return;
    }

    const monthlyRate = annualRate / 12 / 100;
    const months = years * 12;

    const emi = principal * monthlyRate *
        Math.pow(1 + monthlyRate, months) /
        (Math.pow(1 + monthlyRate, months) - 1);

    emiResult.textContent = "Monthly EMI: ₹" +
        emi.toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
}

loanAmountInput.addEventListener("input", calculateEMI);
interestRateInput.addEventListener("input", calculateEMI);
loanTenureInput.addEventListener("input", calculateEMI);