let patient_data = {};
let xray_data = {};
let toaster_success = "rgba(0, 80, 20, 0.9)";
let toaster_info = "rgba(0, 20, 80, 0.9)";
let toaster_alert = "rgba(150, 10, 10, 0.9)";

function show_success(text) {
  return Toastify({
    text: text,
    duration: 5000,
    close: true,
    gravity: "bottom",
    position: "center",
    stopOnFocus: true,
    style: {
      background: "#026443",
      borderRadius: "5px",
      color: "#fffffe",
      boxShadow: "none",
    },
  }).showToast();
}

function show_info(text) {
  return Toastify({
    text: text,
    duration: 5000,
    close: true,
    gravity: "bottom",
    position: "center",
    stopOnFocus: true,
    style: {
      background: "#025464",
      borderRadius: "5px",
      color: "#fffffe",
      boxShadow: "none",
    },
  }).showToast();
}

function show_alert(text) {
  return Toastify({
    text: text,
    duration: 5000,
    close: true,
    gravity: "bottom",
    position: "center",
    stopOnFocus: true,
    style: {
      background: "#f98080",
      borderRadius: "5px",
      color: "#fffffe",
      boxShadow: "none",
    },
  }).showToast();
}
