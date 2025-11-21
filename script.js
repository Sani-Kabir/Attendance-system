async function markAttendance() {
    const name = document.getElementById("studentName").value;

    if (name.trim() === "") {
        alert("Please enter a name!");
        return;
    }

    const response = await fetch("/mark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name })
    });

    const data = await response.json();
    alert(data.message);
    document.getElementById("studentName").value = "";
}

async function loadAttendance() {
    const response = await fetch("/attendance");
    const records = await response.json();

    const tableBody = document.getElementById("attendanceTableBody");
    tableBody.innerHTML = "";

    for (let record of records) {
        const row = `<tr>
                        <td>${record.name}</td>
                        <td>${record.time}</td>
                    </tr>`;
        tableBody.innerHTML += row;
    }
}

// Load attendance on page start
loadAttendance();
