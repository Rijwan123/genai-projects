const API_URL = "http://127.0.0.1:8000";


// -----------------------------
// TEXT SUMMARIZATION
// -----------------------------

export async function summarizeText(text) {

  const formData = new FormData();

  formData.append("text", text);

  const response = await fetch(
    `${API_URL}/summarize`,
    {
      method: "POST",
      body: formData,
    }
  );


  const data = await response.json();


  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.summary ||
      "Failed to summarize text"
    );
  }


  return data;
}


// -----------------------------
// IMAGE EXPLANATION
// -----------------------------

export async function explainImage(file) {

  const formData = new FormData();

  formData.append("file", file);


  const response = await fetch(
    `${API_URL}/explain-image`,
    {
      method: "POST",
      body: formData,
    }
  );


  const data = await response.json();


  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.explanation ||
      "Failed to analyze image"
    );
  }


  return data;
}


// -----------------------------
// CHAT
// -----------------------------

export async function sendChatMessage(message) {

  const formData = new FormData();

  formData.append(
    "message",
    message
  );


  const response = await fetch(
    `${API_URL}/chat`,
    {
      method: "POST",
      body: formData,
    }
  );


  const data = await response.json();


  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.response ||
      "Chat request failed"
    );
  }


  return data;
}