from flask import Flask, request, jsonify, render_template
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
import os

# Ensure NLTK stopwords available (download if needed)
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

pstem = PorterStemmer()

def Stemmer(contents: str) -> str:
    """
    Preprocessing identical to training:
    - keep letters only
    - lowercase
    - split, remove stopwords
    - porter stem
    """
    if contents is None:
        return ""
    text = re.sub('[^a-zA-Z]', ' ', contents)
    text = text.lower()
    words = text.split()
    words = [pstem.stem(w) for w in words if w not in stop_words]
    return ' '.join(words)

app = Flask(__name__, static_folder="static", template_folder="templates")

# --- Load model + vectorizer (use your actual filenames) ---
MODEL_FILENAME = "fake_news_model.joblib"
VECT_FILENAME  = "tfidf_vectorizer.joblib"

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, MODEL_FILENAME)
vect_path  = os.path.join(base_dir, VECT_FILENAME)

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")
if not os.path.exists(vect_path):
    raise FileNotFoundError(f"Vectorizer file not found at {vect_path}")

model = joblib.load(model_path)
vect  = joblib.load(vect_path)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts JSON with:
      { "author": "...", "title": "..." }
    Combines author + title (only) to form the text used for prediction.
    Returns JSON: { prediction: 0|1, label: "Real"/"Fake", confidence: float, processed_preview: str }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    author = (data.get("author") or "").strip()
    title  = (data.get("title") or "").strip()

    contents_raw = " ".join([author, title]).strip()
    if contents_raw == "":
        return jsonify({"error": "Provide at least one of 'author' or 'title'"}), 400

    processed = Stemmer(contents_raw)

    try:
        X = vect.transform([processed])
    except Exception as e:
        return jsonify({"error": f"Vectorizer transform failed: {str(e)}"}), 500

    try:
        pred = int(model.predict(X)[0])
    except Exception as e:
        return jsonify({"error": f"Model prediction failed: {str(e)}"}), 500

    confidence = None
    try:
        probs = model.predict_proba(X)
        confidence = float(probs.max())
    except Exception:
        confidence = None

    label = "Fake" if pred == 1 else "Real"

    return jsonify({
        "prediction": pred,
        "label": label,
        "confidence": confidence,
        "processed_preview": processed[:600]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
