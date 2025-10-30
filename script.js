// Simple SpiritBridge Script

// Daily verse list
const verses = [
  "Philippians 4:13 - I can do all things through Christ who strengthens me.",
  "Jeremiah 29:11 - For I know the plans I have for you, declares the Lord.",
  "Psalm 23:1 - The Lord is my shepherd, I shall not want.",
  "Isaiah 40:31 - Those who hope in the Lord will renew their strength.",
  "Romans 8:28 - All things work together for good to those who love God."
];

// Display random verse
function showVerse() {
  const random = Math.floor(Math.random() * verses.length);
  document.getElementById("verse").innerText = verses[random];
}

// Simple login
function login() {
  const name = document.getElementById("name").value.trim();
  const pin = document.getElementById("pin").value.trim();

  if (pin === "center2025" && name !== "") {
    document.getElementById("login").style.display = "none";
    document.getElementById("app").style.display = "block";
    document.getElementById("username").innerText = name;
    showVerse();
  } else {
    alert("Invalid name or PIN. Try again.");
  }
}

// Ethan AI
function sendMessage() {
  const input = document.getElementById("userInput");
  const chat = document.getElementById("chat");

  if (input.value.trim() === "") return;

  const userMsg = document.createElement("div");
  userMsg.classList.add("message");
  userMsg.innerText = "🧍 " + input.value;
  chat.appendChild(userMsg);

  // Ethan’s response logic
  const reply = document.createElement("div");
  reply.classList.add("message");
  reply.style.background = "rgba(0,200,255,0.3)";
  
  const responses = [
    "Ethan 🤖: Remember, God’s timing is perfect ⏳",
    "Ethan 🤖: Be still — the Lord is fighting for you 💪",
    "Ethan 🤖: Faith doesn’t make things easy, it makes them possible 🙏",
    "Ethan 🤖: You are loved beyond measure ❤️",
    "Ethan 🤖: Prayer changes things. Don’t stop praying! 🙌"
  ];
  
  reply.innerText = responses[Math.floor(Math.random() * responses.length)];
  chat.appendChild(reply);

  input.value = "";
  chat.scrollTop = chat.scrollHeight;
    }
