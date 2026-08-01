document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/health")
        .then(res => res.json())
        .then(data => console.log("System Health Check:", data))
        .catch(err => console.error("Health check error:", err));
});

// Interactive alert function
window.dispatchStaff = function() {
    alert("🚀 Priority Alert Triggered!\n\nSMS & WhatsApp alert containing camera coordinates sent to cleaning staff (Location: Main Gate Plaza - Bin #102).");
};