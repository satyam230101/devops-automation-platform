
const form = document.getElementById("employeeForm");
const employeeList = document.getElementById("employeeList");
const message = document.getElementById("message");
const search = document.getElementById("search");

const employeeId = document.getElementById("employeeId");
const formTitle = document.getElementById("formTitle");
const submitButton = document.getElementById("submitButton");
const cancelButton = document.getElementById("cancelButton");

let employees = [];

async function loadEmployees() {
    try {
        const response = await fetch("/api/employees");

        if (!response.ok) {
            throw new Error("Could not load employees");
        }

        employees = await response.json();
        displayEmployees(employees);

    } catch (error) {
        message.textContent = error.message;
    }
}

function displayEmployees(data) {
    employeeList.innerHTML = "";

    data.forEach(employee => {
        const row = document.createElement("tr");

        const values = [
            employee.id,
            employee.name,
            employee.email,
            employee.department,
            employee.designation
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const actionCell = document.createElement("td");

        // Edit button
        const editButton = document.createElement("button");
        editButton.textContent = "Edit";

        editButton.addEventListener("click", () => {
            editEmployee(employee);
        });

        // Delete button
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-btn";

        deleteButton.addEventListener("click", () => {
            deleteEmployee(employee.id);
        });

        actionCell.appendChild(editButton);
        actionCell.appendChild(deleteButton);

        row.appendChild(actionCell);
        employeeList.appendChild(row);
    });
}

// Load employee details into the form
function editEmployee(employee) {
    employeeId.value = employee.id;

    document.getElementById("name").value = employee.name;
    document.getElementById("email").value = employee.email;
    document.getElementById("department").value = employee.department;
    document.getElementById("designation").value = employee.designation;

    formTitle.textContent = "Edit Employee";
    submitButton.textContent = "Update Employee";
    cancelButton.style.display = "block";

    message.textContent = "";

    form.scrollIntoView({ behavior: "smooth" });
}

// Reset the form to Add Employee mode
function resetForm() {
    form.reset();
    employeeId.value = "";

    formTitle.textContent = "Add Employee";
    submitButton.textContent = "Add Employee";
    cancelButton.style.display = "none";
}

cancelButton.addEventListener("click", resetForm);

// Add or Update employee
form.addEventListener("submit", async event => {
    event.preventDefault();

    const employee = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        department: document.getElementById("department").value,
        designation: document.getElementById("designation").value
    };

    const id = employeeId.value;

    const url = id
        ? `/api/employees/${id}`
        : "/api/employees";

    const method = id ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(employee)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Operation failed");
        }

        message.textContent = result.message;

        resetForm();
        await loadEmployees();

    } catch (error) {
        message.textContent = error.message;
    }
});

// Delete employee
async function deleteEmployee(id) {
    if (!confirm("Are you sure you want to delete this employee?")) {
        return;
    }

    try {
        const response = await fetch(`/api/employees/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not delete employee");
        }

        message.textContent = result.message;

        resetForm();
        await loadEmployees();

    } catch (error) {
        message.textContent = error.message;
    }
}

// Search employees
search.addEventListener("input", () => {
    const query = search.value.toLowerCase();

    const filtered = employees.filter(employee =>
        employee.name.toLowerCase().includes(query) ||
        employee.department.toLowerCase().includes(query)
    );

    displayEmployees(filtered);
});

loadEmployees();
