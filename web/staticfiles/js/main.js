function login(e, elem) {
  e.preventDefault();
  const body = JSON.stringify({
    email: elem.querySelector("[name=email]").value.trim(),
    password: elem.querySelector("[name=password]").value.trim(),
  });
  console.log(
    elem.querySelector("[name=password]").value.trim(),
    elem.querySelector("[name=email]").value.trim()
  );
  fetch("/signin/", {
    method: "POST",
    headers: {
      "X-CSRFToken": document
        .querySelector("input[name=csrfmiddlewaretoken]")
        .value.trim(),
    },
    body,
  })
    .then((res) => res.json())
    .then((res) => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const nextpage = urlParams.get("next");
        if (res.status === 200) {
          show_success(res.message);
          setTimeout(() => {
            window.location.href = nextpage ? nextpage : "/";
          }, 2000);
        }
        if (res.status === 401) {
          show_alert(res.message);
          return;
        }
      } catch (e) {}
    })
    .catch((e) => console.log(e));
}

function register(elem, event) {
  event.preventDefault();
  let data = {};
  Array.from(elem.querySelectorAll("input")).forEach((input) => {
    data[input.name] = input.value;
  });
  fetch("/signup/", {
    method: "post",
    headers: {
      "X-CSRFToken": document
        .querySelector("input[name=csrfmiddlewaretoken]")
        .value.trim(),
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data && data.status && data.status == 200) {
        show_success("Account created successfully");
        setTimeout(() => {
          window.location.href = "/";
        }, 2000);
      } else {
        if (data && data.message) {
          show_alert(data.message);
        }
      }
    })
    .catch((e) => console.log(e));
}
function addPatient(elem, event) {
  event.preventDefault();
  const body = new FormData();
  Array.from(elem.querySelectorAll("input,textarea,select")).forEach(
    (input) => {
      if (input.type === "radio") {
        if (input.checked) {
          body.append(input.name, input.value);
        }
      } else if (input.type === "file") {
        body.append("image", input.files[0]);
      } else {
        body.append(input.name, input.value);
      }
    }
  );
  fetch("/patients/add-patient/", {
    method: "POST",
    headers: {
      "X-CSRFToken": document
        .querySelector("input[name=csrfmiddlewaretoken]")
        .value.trim(),
    },
    body,
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.status == 200) {
        show_success(res["message"]);
        setTimeout(() => {
          window.location.href = "/patients/my-patients";
        }, 3000);
      } else {
        show_alert(res["message"]);
      }
    });
}

function modifyPatient(event, patient_id) {
  event.preventDefault();
  patient_data["gender"] = document.querySelector(
    'input[name="gender"]:checked'
  ).value;
  console.log(patient_data);
  console.log(patient_id);
  const body = new FormData();
  for (let key in patient_data) {
    body.append(key, patient_data[key]);
  }
  if (patient_data["image"]) {
    body.append("image", patient_data["image"]);
  }
  fetch(`/patients/${patient_id}/edit-patient/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": document
        .querySelector("input[name=csrfmiddlewaretoken]")
        .value.trim(),
    },
    body,
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.status == 200) {
        show_success(res["message"]);
        setTimeout(() => {
          window.location.href = "/patients/my-patients";
        }, 3000);
      } else {
        show_alert(res["message"]);
      }
    });
}

function startFlServer() {
  console.log("server started");

  const outputDiv = document.getElementById("output");
  async function connectWebSocket() {
    var socket = new WebSocket("ws://localhost:7000/ws");

    socket.onopen = function (event) {
      show_info("Starting Federated learning server ....");
    };

    socket.onmessage = function (event) {
      const data = JSON.parse(event.data);
      console.log(data.type);
      console.log(data.text);
      if (data.type === "warning") {
        outputDiv.innerHTML +=
          "<p class='bg-red-400 text-white w-full px-2 py-4'>" +
          data.text +
          "</p>";
      } else if (data.type === "success") {
        outputDiv.innerHTML +=
          "<p class='bg-green-400 text-white w-full px-2 py-4'>" +
          data.text +
          "</p>";
      } else {
        outputDiv.innerHTML +=
          "<p class='bg-blue-400 text-white w-full px-2 py-4'>" +
          data.text +
          "</p>";
      }
    };

    socket.onclose = function (event) {
      show_success("Federated learning process done!");
    };

    socket.onerror = function (event) {
      show_error("An error has occurred, please verify and try again");
    };
  }

  connectWebSocket();
}

function addXrayImage(event, elem, patient_id) {
  event.preventDefault();
  console.log("hello");
  const body = new FormData();
  let algo = elem.querySelector("[id=algo]").value.trim();
  let diagnostic_input = elem
    .querySelector("[id=diagnostic_input]")
    .value.trim();
  body.append("type", algo);
  body.append("diagnostic", diagnostic_input);
  if (xray_data["image"]) {
    body.append("image", xray_data["image"]);
  } else {
    return show_alert("You need to add an xray image !");
  }
  fetch(`/patients/xray-image/${patient_id}/add-xray-image`, {
    method: "POST",
    headers: {
      "X-CSRFToken": document
        .querySelector("input[name=csrfmiddlewaretoken]")
        .value.trim(),
    },
    body,
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.status == 200) {
        show_success(res["message"]);
        setTimeout(() => {
          window.location.href = `/patients/${patient_id}/edit-patient/`;
        }, 3000);
      } else {
        show_alert(res["message"]);
      }
    });
}

function editXrayImage(event, elem, xray_image_id) {
  event.preventDefault();
  console.log(xray_image_id);
  const body = new FormData();
  let algo = elem.querySelector("[id=algo]").value.trim();
  let diagnostic_input = elem
    .querySelector("[id=diagnostic_input]")
    .value.trim();
  body.append("type", algo);
  body.append("diagnostic", diagnostic_input);
  if (xray_data["image"]) {
    body.append("image", xray_data["image"]);
  }

  fetch(`/patients/xray-image/edit-xray-image/${xray_image_id}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": document
        .querySelector("input[name=csrfmiddlewaretoken]")
        .value.trim(),
    },
    body,
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.status == 200) {
        show_success(res["message"]);
        setTimeout(() => {
          location.reload();
        }, 3000);
      } else {
        show_alert(res["message"]);
      }
    });
}

function sendMessage(event, elem) {
  event.preventDefault();

  const body = new FormData();

  let email = elem.querySelector("[id=email]").value.trim();
  let subject = elem.querySelector("[id=subject]").value.trim();
  let message = elem.querySelector("[id=message]").value.trim();

  body.append("email", email);
  body.append("subject", subject);
  body.append("message", message);

  fetch(`/contact-us`, {
    method: "POST",
    headers: {
      "X-CSRFToken": document
        .querySelector("input[name=csrfmiddlewaretoken]")
        .value.trim(),
    },
    body,
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.status == 200) {
        show_success(res["message"]);
        setTimeout(() => {
          location.reload();
        }, 3000);
      } else {
        show_alert(res["message"]);
      }
    });
}
