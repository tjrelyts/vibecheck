const form = document.getElementById("sentiment-form");
const clearButton = document.getElementById("clear-btn");
const messageHistory = document.getElementById("message-history");
let maxMessages = 5;

// Function to update max messages based on screen size
function updateMaxMessages() {
  if (window.innerWidth < 1024) { 
    maxMessages = 3;
  } else {
    maxMessages = 5;
  }
  
  // Trim existing messages if needed
  while (messageHistory.children.length > maxMessages) {
    messageHistory.removeChild(messageHistory.firstChild);
  }
  
  // Update localStorage to match
  const messages = Array.from(messageHistory.children).map((child) => {
    return {
      message: child.children[0].textContent,
      analysis: child.children[1].textContent,
      timestamp: new Date(child.children[2].textContent).getTime(),
    };
  });
  localStorage.setItem("messages", JSON.stringify(messages));
}

document.addEventListener("DOMContentLoaded", function () {
  function loadMessages() {
    const messages = JSON.parse(localStorage.getItem("messages")) || [];
    // Only load up to maxMessages
    messages.slice(-maxMessages).forEach((item) => {
      const listItem = createMessageItem(
        item.message,
        item.analysis,
        item.timestamp
      );
      messageHistory.appendChild(listItem);
    });
  }

  // Update max messages and load messages
  updateMaxMessages();
  loadMessages();

  function createMessageItem(message, analysis, timestamp) {
    const listItem = document.createElement("li");
    listItem.className = "list-group-item d-flex justify-content-between";

    const messageDiv = document.createElement("div");
    messageDiv.id = "message";
    messageDiv.textContent = message;

    const analysisDiv = document.createElement("div");
    analysisDiv.id = "analysis";
    analysisDiv.textContent = analysis;

    const timestampDiv = document.createElement("div");
    timestampDiv.id = "timestamp";
    timestampDiv.textContent = new Date(timestamp).toLocaleString();

    listItem.appendChild(messageDiv);
    listItem.appendChild(analysisDiv);
    listItem.appendChild(timestampDiv);

    return listItem;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const msgInput = document.getElementById("msg");
    const message = msgInput.value.trim();

    if (message !== "") {
      analyzeSentiment(message, (sentiment) => {
        const timestamp = Date.now();
        const listItem = createMessageItem(message, sentiment, timestamp);
        messageHistory.appendChild(listItem);

        if (messageHistory.children.length > maxMessages) {
          messageHistory.removeChild(messageHistory.firstChild);
        }

        const messages = Array.from(messageHistory.children).map((child) => {
          return {
            message: child.children[0].textContent,
            analysis: child.children[1].textContent,
            timestamp: new Date(child.children[2].textContent).getTime(),
          };
        });
        localStorage.setItem("messages", JSON.stringify(messages));

        msgInput.value = "";
      });
    }
  });

  clearButton.addEventListener("click", function () {
    localStorage.clear();
    messageHistory.innerHTML = "";
  });
});

function analyzeSentiment(message, callback) {
  fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ msg: message }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Update the result first
      updatePage(data.sentiment);
      // Then call the callback for history update
      callback(data.sentiment);
    })
    .catch((error) => {
      console.error("Error:", error);
      // Show error in result
      let result = document.getElementById("sentiment-result");
      result.textContent = "❌ Error analyzing sentiment";
      result.classList.add("show");
    });
}

function updatePage(sentiment) {
  let body = document.querySelector("body");
  let icon = document.querySelector('link[rel="icon"]');
  let result = document.getElementById("sentiment-result");

  // First remove show class to trigger animation
  result.classList.remove("show");
  
  // Update after a small delay to allow animation
  setTimeout(() => {
    switch (sentiment) {
      case "positive":
        body.classList.remove("bg-dark", "bg-danger");
        body.classList.add("bg-success");
        icon.href = "/static/assets/favicon1.ico";
        result.textContent = "😊 Positive";
        break;
      case "negative":
        body.classList.remove("bg-dark", "bg-success");
        body.classList.add("bg-danger");
        icon.href = "/static/assets/favicon2.ico";
        result.textContent = "😔 Negative";
        break;
      default:
        body.classList.remove("bg-danger", "bg-success");
        body.classList.add("bg-dark");
        icon.href = "/static/assets/favicon0.ico";
        result.textContent = "😐 Neutral";
        break;
    }
    
    // Add show class to trigger animation
    result.classList.add("show");
  }, 100);
}

function setCharacterLimit() {
  const windowWidth = window.innerWidth;
  const msgInput = document.getElementById("msg");

  if (windowWidth <= 768) {
    msgInput.setAttribute("maxlength", "40");
    clearButton.click();
  } else {
    msgInput.setAttribute("maxlength", "100");
  }
}

setCharacterLimit();

window.addEventListener("resize", function() {
  updateMaxMessages();
  setCharacterLimit();
});
