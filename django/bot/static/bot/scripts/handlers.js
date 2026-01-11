"use strict";
import { getCsrfToken, handleRequest } from "./helpers.js";

const app_state = [];

export async function handleUserInput(event, input) {
  try {
    console.log("==================handle user input====================");
    event.preventDefault();

    const user_message = input.value;

    if (!user_message) return;

    // update state
    app_state.push({ sender: "user", text: user_message });

    const csrfToken = getCsrfToken();
    const body_content = JSON.stringify({ user_message });

    // send user message to backend
    const headers_content = {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    };
    const data = await handleRequest(headers_content, body_content);
    console.log(data);

    if (data.status === "success") {
      const { response } = data;

      // update state
      app_state.push({
        sender: "bot",
        text: response.text,
        buttons: response.is_btn ? response.buttons : [],
      });

      renderChat();
    }
    input.value = "";
  } catch (error) {
    console.log(error);
  }
}

export async function handleBtnInputs(event) {
  try {
    const btn = event.target.closest(".chat_btn");
    if (!btn) return;

    const payload = btn.dataset.payload;
    const csrfToken = getCsrfToken();
    const body_content = JSON.stringify({ user_message: payload });

    const headers_content = {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    };
    const data = await handleRequest(headers_content, body_content);
    console.log(data);
  } catch (error) {
    console.log(error);
  }
}

function renderChat() {
  const chat_container = document.getElementById("chat_container");

  const chat_markup = app_state
    .map((entry) => {
      if (entry.sender === "user") {
        return `
          <div class="chatbot__chats-user chatbot__chats-resp">
            <p>${entry.text}</p>
          </div>
        `;
      }

      if (entry.sender === "bot") {
        console.log(entry);
        let btn_markup = "";

        if (entry.buttons.length > 0) {
          btn_markup = entry.buttons
            .map(
              (btn) =>
                `<button class="chat_btn" data-payload="${btn.payload}">
                  ${btn.title}
                </button>`
            )
            .join("");
        }

        return `
          <div class="chatbot__chats-bot chatbot__chats-resp">
            <div class="chatbot-response-box">
              <p class="bot-msg-text">${entry.text}</p>
              <div class="chat_btns bot-btns">
                ${btn_markup}
              </div>
            </div>
          </div>
        `;
      }

      return "";
    })
    .join("");

  chat_container.innerHTML = chat_markup;
  chat_container.scrollIntoView;
}
