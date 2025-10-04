// main.js - (author + title only) with disabled Predict when both empty

const predictBtn = document.getElementById("predictBtn");
const clearBtn = document.getElementById("clearBtn");
const authorEl = document.getElementById("author");
const titleEl = document.getElementById("title");
const resultDiv = document.getElementById("result");
const labelEl = document.getElementById("label");
const confEl = document.getElementById("confidence");
const processedEl = document.getElementById("processed");

// enable/disable Predict button depending on inputs
function updatePredictEnabled() {
  const author = (authorEl.value || "").trim();
  const title = (titleEl.value || "").trim();
  const enabled = author.length > 0 || title.length > 0;
  predictBtn.disabled = !enabled;
  predictBtn.style.opacity = enabled ? "1" : "0.6";
}

authorEl.addEventListener("input", updatePredictEnabled);
titleEl.addEventListener("input", updatePredictEnabled);

predictBtn.addEventListener("click", makePrediction);
clearBtn.addEventListener("click", clearInputs);

function showResult(data) {
  resultDiv.classList.remove("hidden");

  labelEl.innerText = `Prediction: ${data.label} (${data.prediction})`;
  // Color label: Real => teal/green, Fake => orange
  labelEl.style.color = data.label === "Fake" ? "#ff922b" : "#20c997";

  confEl.innerText = data.confidence !== null && data.confidence !== undefined
    ? `Confidence: ${(data.confidence * 100).toFixed(1)}%`
    : "Confidence: N/A";

  processedEl.innerText = `Processed preview:\n${data.processed_preview || ""}`;
}

function hideResult() {
  resultDiv.classList.add("hidden");
  labelEl.innerText = "";
  confEl.innerText = "";
  processedEl.innerText = "";
}

function clearInputs() {
  authorEl.value = "";
  titleEl.value = "";
  updatePredictEnabled();
  hideResult();
  authorEl.focus();
}

async function makePrediction() {
  const author = authorEl.value || "";
  const title = titleEl.value || "";

  if (!author.trim() && !title.trim()) {
    // should not happen because button disabled, but guard anyway
    alert("Please enter at least an author or a title.");
    return;
  }

  // disable while waiting
  predictBtn.disabled = true;
  predictBtn.style.opacity = "0.7";

  try {
    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ author: author, title: title })
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ error: resp.statusText }));
      alert("Prediction failed: " + (err.error || resp.statusText));
      return;
    }

    const data = await resp.json();
    showResult(data);
  } catch (e) {
    alert("Network or server error: " + e.message);
  } finally {
    updatePredictEnabled();
  }
}

// run initial state
updatePredictEnabled();
