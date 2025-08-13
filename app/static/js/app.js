// ====== Main JavaScript for Student Portal ======

// Show alert messages automatically fade after 3 seconds
document.addEventListener("DOMContentLoaded", function () {
    let alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });
});

// Confirmation before deleting an item
function confirmDelete(message = "Are you sure you want to delete this item?") {
    return confirm(message);
}

// Dynamic form example (future use)
function updateFormOptions(endpoint, targetSelectId) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById(targetSelectId);
            select.innerHTML = "";
            data.forEach(option => {
                let opt = document.createElement("option");
                opt.value = option.id;
                opt.textContent = option.name;
                select.appendChild(opt);
            });
        })
        .catch(error => console.error("Error loading options:", error));
}
