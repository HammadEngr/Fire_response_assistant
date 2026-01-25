"use strict";
import { getCsrfToken, handleRequest, getLocation } from "./helpers.js";

const app_state = [];

export async function handleSendLocation() {
  try {
    const { latitude, longitude } = await getLocation();

    const body_content = JSON.stringify({ latitude, longitude });
    const csrfToken = getCsrfToken();
    const headers_content = {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    };

    const res = await fetch("send_location/", {
      method: "POST",
      credentials: "same-origin",
      body: body_content,
      headers: headers_content,
    });
    const result = await res.json();
  } catch (error) {
    console.log(error);
  }
}

export async function handleUserInput(event, input) {
  try {
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

    if (data.status === "success") {
      const { response } = data;

      // Handle multiple messages from Rasa
      if (Array.isArray(response)) {
        response.forEach((msg) => {
          app_state.push(msg);
        });
      } else {
        // Fallback for single message (backward compatibility)
        app_state.push({
          sender: "bot",
          text: response.text,
          message_type: response.message_type,
          buttons: response.is_btn ? response.buttons : [],
          data: response.data || null,
        });
      }

      renderChat();
    }
    input.value = "";
  } catch (error) {
    console.log(error);
  }
}

export async function handleBtnInputs(event, btn_class = ".chat_btn") {
  try {
    const btn = event.target.closest(btn_class);
    if (!btn) return;

    const payload = btn.dataset.payload;
    const btnText = btn.textContent.trim();

    app_state.push({ sender: "user", text: btnText });

    const csrfToken = getCsrfToken();
    const body_content = JSON.stringify({ user_message: payload });

    const headers_content = {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    };
    const data = await handleRequest(headers_content, body_content);

    if (data.status === "success") {
      const { response } = data;

      if (Array.isArray(response)) {
        response.forEach((msg) => {
          const msg_text = msg.text.replace(/\n/g, "<br>");
          app_state.push(msg);
        });
      } else {
        // Fallback for single message
        const msg_text = response.text.replace(/\n/g, "<br>");
        app_state.push({
          sender: "bot",
          text: msg_text,
          message_type: response.message_type,
          buttons: response.is_btn ? response.buttons : [],
          data: response.data || null,
        });
      }

      renderChat();
    }
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
        let btn_markup = "";
        if (entry.buttons && entry.buttons.length > 0) {
          btn_markup = entry.buttons
            .map(
              (btn) =>
                `<button class="chat_btn" data-payload='${btn.payload}'>
                  ${btn.title}
                </button>`,
            )
            .join("");
        }
        if (entry.message_type === "custom") {
          let sections = entry.sections.map((sec) => {
            return {
              heading: sec.heading ?? "",
              content: sec.content
                ?.replace(/\\n/g, "<br>")
                ?.replace(/\r\n/g, "<br>")
                ?.replace(/\n/g, "<br>"),
            };
          });
          return renderCustomMessage(
            entry.title,
            sections,
            entry.text,
            entry.footer,
            btn_markup,
          );
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
  chat_container.scrollTop = chat_container.scrollHeight;
}

function renderCustomMessage(title, sections, text, footer, btn_markup) {
  return `
    <div class="chatbot__chats-bot chatbot__chats-resp">
      <div class="chatbot-response-box custom-message">
      <div class = "chatbot-response-box-sections-box">
      <h4 class="chatbot-response-box-title" >${title || "Emergency Instructions"}</h4>
        ${sections
          .map(
            (sec) => `
            <div class = "chatbot-response-box-sections-sub-box">
            <h5 class = "chatbot-response-box-sections-heading">${sec.heading}</h5>
            <p>${sec.content || ""}</p>
            </div>
            `,
          )
          .join("")}
        </div>
        <p>${footer || ""}</p>
        <p>${text}</p>
        <div class="chat_btns bot-btns">
          ${btn_markup}
        </div>
      </div>
    </div>
  `;
}
