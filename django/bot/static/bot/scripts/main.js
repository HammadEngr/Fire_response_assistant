"use strict";

const main_btn = document.getElementById("main-btn");
const input = document.querySelector(".chatbot__input-input");
const bot_text_box = document.getElementById("bot-msg-text");
const bot_btns = document.getElementById("bot-btns");

main_btn.addEventListener("click", async function (e) {
  e.preventDefault();

  const user_message = input.value;

  const csrfToken = getCsrfToken();
  const body_content = JSON.stringify({ user_message });

  // send user message to backend
  const headers_content = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrfToken,
  };
  const data = await handleUserRequest(headers_content, body_content);
  console.log(data);

  if (data.status === "success") {
    const { response } = data;
    bot_text_box.innerHTML = response.text;
    if (response.is_btn) {
      const btn_markup = response.buttons
        .map(
          (btn) =>
            `<button class="chat_btn" data-payload=${btn.payload}>${btn.title}</button>`
        )
        .join("");
      bot_btns.innerHTML = "";
      bot_btns.insertAdjacentHTML("beforeend", btn_markup);
    }
  }
});

//  add event listener to parent div and use event delegation
bot_btns.addEventListener("click", async function (e) {
  if (e.target.matches(".chat_btn")) {
    const payload = e.target.dataset.payload;
    const csrfToken = getCsrfToken();
    const body_content = JSON.stringify({ user_message: payload });

    const headers_content = {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    };
    const data = await handleUserRequest(headers_content, body_content);
    console.log(data);
  }
});

function getCsrfToken() {
  const csrfToken = document.cookie
    .split(";")
    .find((value) => value.includes("csrftoken"))
    .split("=")[1];

  return csrfToken;
}

async function handleUserRequest(headers_content, body_content) {
  try {
    const res = await fetch("http://localhost:8000/api/get_response/", {
      method: "POST",
      credentials: "same-origin",
      body: body_content,
      headers: headers_content,
    });

    return await res.json();
  } catch (error) {
    console.log(error);
    throw error;
  }
}

const showPosition = (position) => {
  console.log(position);
  console.log(
    "Latitude: " +
      position.coords.latitude +
      " Longitude: " +
      position.coords.longitude
  );
};

const get_location = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
};
