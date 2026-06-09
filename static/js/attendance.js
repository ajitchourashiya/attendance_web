const video = document.getElementById("video");

let currentAddress = "Unknown Location";
let currentLatitude = "";
let currentLongitude = "";

/* Start Camera */
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
})
.catch(err => {
    document.getElementById("status").innerText =
        "❌ Camera access denied";
});

/* Get Location + Address */
window.addEventListener("load", getLocation);

async function getLocation() {

    const locationDiv = document.getElementById("location");

    if (!navigator.geolocation) {
        locationDiv.innerHTML = "❌ Geolocation not supported";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async (pos) => {

            currentLatitude = pos.coords.latitude;
            currentLongitude = pos.coords.longitude;

            try {
                const res = await fetch(
                    `https://nominatim.openstreetmap.org/reverse?format=json&lat=${currentLatitude}&lon=${currentLongitude}`
                );

                const data = await res.json();

                currentAddress = data.display_name || "Unknown Location";

                locationDiv.innerHTML = `
                    📍 <strong>Your Location:</strong><br>
                    <a target="_blank"
                       href="https://www.google.com/maps?q=${currentLatitude},${currentLongitude}">
                        ${currentAddress}
                    </a>
                `;

            } catch (err) {
                currentAddress = "Unknown Location";

                locationDiv.innerHTML =
                    "📍 Unable to fetch address";
            }
        },
        () => {
            currentAddress = "Unknown Location";

            locationDiv.innerHTML =
                "❌ Location permission denied";
        }
    );
}

/* Capture Attendance */
async function captureAttendance() {

    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    canvas.getContext("2d").drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {

        const formData = new FormData();

        formData.append("image", blob, "face.jpg");
        formData.append("latitude", currentLatitude);
        formData.append("longitude", currentLongitude);
        formData.append("address", currentAddress);

        try {
            const res = await fetch("/verify-attendance", {
                method: "POST",
                body: formData
            });

            const result = await res.json();

            alert(result.message);

            if (result.status) {
                window.location.href = "/dashboard";
            }

        } catch (err) {
            alert("Error marking attendance");
        }

    }, "image/jpeg");
}