const uploadForm = document.getElementById("uploadForm");
const chatForm = document.getElementById("chatForm");
const fileInput = document.getElementById("fileInput");
const questionInput = document.getElementById("questionInput");
const uploadStatus = document.getElementById("uploadStatus");
const messages = document.getElementById("messages");

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split("; ") : [];
    for (const cookie of cookies) {
        const [key, ...rest] = cookie.split("=");
        if (key === name) {
            return decodeURIComponent(rest.join("="));
        }
    }
    return "";
}

function addMessage(text, sender) {
    const node = document.createElement("article");
    node.className = `bubble bubble--${sender}`;
    node.textContent = text;
    messages.appendChild(node);
    messages.scrollTop = messages.scrollHeight;
}

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    uploadStatus.classList.remove("error");

    if (!fileInput.files.length) {
        uploadStatus.textContent = "Select a file first.";
        uploadStatus.classList.add("error");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    uploadStatus.textContent = "Uploading document...";

    try {
        const response = await fetch("/api/upload/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || data.detail || "Upload failed");
        }

        uploadStatus.textContent = `Uploaded. Loaded ${data.chars_loaded} characters.`;
        addMessage("Document ready. Ask your first question.", "bot");
    } catch (error) {
        uploadStatus.textContent = error.message;
        uploadStatus.classList.add("error");
    }
});

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();
    if (!question) {
        return;
    }

    addMessage(question, "user");
    questionInput.value = "";

    try {
        const response = await fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ question }),
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || data.detail || "Request failed");
        }

        addMessage(data.answer, "bot");
    } catch (error) {
        addMessage(error.message, "bot");
    }
});

