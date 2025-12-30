"use strict";
import { getCsrfToken, handleRequest } from "./helpers.js";

export async function handleUserInput(event, bot_text_box, bot_btns, input) {
  try {
    event.preventDefault();

    const user_message = input.value;
    console.log(user_message.length);
    if (!user_message) return;

    const csrfToken = getCsrfToken();
    const body_content = JSON.stringify({ user_message });

    // send user message to backend
    const headers_content = {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    };
    const data = await handleRequest(headers_content, body_content);

    if (data.status === "success") {
      const { response } = data;
      bot_text_box.textContent = response.text;

      console.log(response);
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
  } catch (error) {
    console.log(error);
  }
}

export async function handleBtnInputs(event) {
  try {
    if (event.target.matches(".chat_btn")) {
      const payload = event.target.dataset.payload;
      const csrfToken = getCsrfToken();
      const body_content = JSON.stringify({ user_message: payload });

      const headers_content = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      };
      const data = await handleRequest(headers_content, body_content);
      console.log(data);
    }
  } catch (error) {
    console.log(error);
  }
}
