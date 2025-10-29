function sendMessage() {
  const input = document.getElementById("userInput");
  const msgBox = document.getElementById("messages");
  const userText = input.value.trim();

  if (userText === "") return;

  const userMsg = document.createElement("div");
  userMsg.textContent = "You: " + userText;
  msgBox.appendChild(userMsg);

  const ethanReply = document.createElement("div");
  ethanReply.textContent = "Ethan: I'm here to help! (Real responses coming soon...)";
  msgBox.appendChild(ethanReply);

  input.value = "";
  msgBox.scrollTop = msgBox.scrollHeight;
}
