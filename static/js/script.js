const userSelect = document.getElementById("userSelect");
const profileImg = document.getElementById("profileImg");
const testImage = document.getElementById("testImage");
const previewImg = document.getElementById("previewImg");
const result = document.getElementById("result");

// Load profile image when select changes
userSelect.addEventListener("change", () => {
    const userId = userSelect.value;
    if (!userId) {
        profileImg.src = "";
        return;
    }
    profileImg.src = `/assets/${userId}.jpg`;
});

// Preview uploaded image
testImage.addEventListener("change", () => {
    const file = testImage.files[0];
    if (file) {
        previewImg.src = URL.createObjectURL(file);
    }
});

// Send to backend for verification
async function verify() {
    const userId = userSelect.value;
    const file = testImage.files[0];

    if (!userId || !file) {
        result.innerHTML = "Please select user and upload photo.";
        result.style.color = "red";
        return;
    }

    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("image", file);

    const res = await fetch("/verify", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (data.match === true) {
        result.innerHTML = "✔ MATCH — Absensi Berhasil";
        result.style.color = "green";
    } else {
        result.innerHTML = "✖ NOT MATCH — Wajah Tidak Cocok";
        result.style.color = "red";
    }
}
