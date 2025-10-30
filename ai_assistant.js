// ai_assistant.js

async function askAI(prompt) {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer YOUR_API_KEY_HERE",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "You are a friendly assistant for the PCEA Center Youth app." },
        { role: "user", content: prompt }
      ]
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example usage
async function handleAIMessage() {
  const userInput = document.getElementById("ai-input").value;
  const reply = await askAI(userInput);
  document.getElementById("ai-reply").innerText = reply;
}
