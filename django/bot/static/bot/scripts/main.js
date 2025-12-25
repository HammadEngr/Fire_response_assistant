"use strict";

const main_btn = document.getElementById("main-btn");
const input = document.querySelector(".chatbot__input-input");

main_btn.addEventListener("click", async function (e) {
  e.preventDefault();

  // get user message
  const user_message = input.value;

  // get csrf token from cookies (Django requirement)
  const csrfToken = document.cookie
    .split(";")
    .find((value) => value.includes("csrftoken"))
    .split("=")[1];

  const body_content = JSON.stringify({ user_message });

  // send user message to backend
  const res = await fetch("http://localhost:8000/api/get_response/", {
    method: "POST",
    credentials: "same-origin",
    body: body_content,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  });

  // get response data
  const data = await res.json();

  console.log(data);
});
