let allData = [];

/* LOAD DATA */
async function loadAttendance() {

    try {

        const response = await fetch("/api/view-attendance", {
            credentials: "include"
        });

        const result = await response.json();

        if (!result.success) {
            alert(result.message);
            return;
        }

        allData = result.data; // store globally
        renderTable(allData);

    } catch (err) {
        console.error(err);
        alert("Failed to load attendance");
    }
}

/* RENDER TABLE */
function renderTable(data) {

    const table = document.getElementById("attendanceTable");
    table.innerHTML = "";

    if (data.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="7" style="text-align:center;">
                    No Records Found
                </td>
            </tr>
        `;
        return;
    }

    data.forEach(item => {

        const mapLink = item.latitude && item.longitude
            ? `https://www.google.com/maps?q=${item.latitude},${item.longitude}`
            : "#";

        table.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>${item.date}</td>
                <td>${item.status}</td>
                <td>${item.latitude}</td>
                <td>${item.longitude}</td>
                <td>
                    <a href="${mapLink}" target="_blank">
                        ${item.address || "-"}
                    </a>
                </td>
                <td>${item.date_time}</td>
            </tr>
        `;
    });
}

/* APPLY FILTER */
function applyFilter() {

    const name = document.getElementById("nameFilter")?.value.toLowerCase() || "";
    const startDate = document.getElementById("startDate")?.value;
    const endDate = document.getElementById("endDate")?.value;

    let filtered = allData;

    // NAME FILTER
    if (name) {
        filtered = filtered.filter(item =>
            item.name.toLowerCase().includes(name)
        );
    }

    // START DATE FILTER
    if (startDate) {
        filtered = filtered.filter(item =>
            item.date >= startDate
        );
    }

    // END DATE FILTER
    if (endDate) {
        filtered = filtered.filter(item =>
            item.date <= endDate
        );
    }

    renderTable(filtered);
}

/* RESET FILTER */
function resetFilter() {

    document.getElementById("nameFilter").value = "";
    document.getElementById("startDate").value = "";
    document.getElementById("endDate").value = "";

    renderTable(allData);
}

/* INIT */
loadAttendance();