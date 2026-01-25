"use strict";
import {
  handleBtnInputs,
  handleUserInput,
  handleSendLocation,
} from "./handlers.js";

const user_input = document.getElementById("user_msg");
const send_message_btn = document.getElementById("send_message_btn");
const chat_container = document.getElementById("chat_container");
const quick_section = document.querySelector(".quick-section");

// EVENT LISTENERS
// Handle User location on page load
document.addEventListener("DOMContentLoaded", async function () {
  handleSendLocation();
});

// Handle User input on button click and Enter key press
send_message_btn.addEventListener("click", function (e) {
  handleUserInput(e, user_input);
});
user_input.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    handleUserInput(e, user_input);
  }
});

// Handle Chat Container button clicks
chat_container.addEventListener("click", function (e) {
  handleBtnInputs(e);
});

// Handle Quick Section button clicks
quick_section.addEventListener("click", function (e) {
  handleBtnInputs(e, ".quick-btn");
});
