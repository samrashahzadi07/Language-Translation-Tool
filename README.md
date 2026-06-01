# 🌐 LinguaFlow — Language Translation Tool
### CodeAlpha AI Internship · Task 1

A sleek, production-ready language translation web app built with **Streamlit** and **Google Translate API** (via `deep-translator`).

---

## ✨ Features

- **50+ Languages** supported including Urdu, Hindi, Arabic, Chinese, French, Spanish and more
- **Auto-detect** source language
- **Translation history** (last 10 translations shown)
- **Word & character count** for translated output
- **One-click copy** via Streamlit's code block
- **Response time** indicator
- Clean dark-themed UI with gradient design

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🛠️ Tech Stack

| Component         | Technology              |
|-------------------|-------------------------|
| UI Framework      | Streamlit               |
| Translation API   | Google Translate (via `deep-translator`) |
| Language          | Python 3.8+             |
| Styling           | Custom CSS              |

---

## 📁 Project Structure

```
CodeAlpha_LanguageTranslationTool/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 📸 How It Works

1. User enters text in the input box
2. Selects source language (or uses Auto Detect)
3. Selects target language
4. Clicks **Translate**
5. Translated text appears with word/char count and response time

---

## 👤 Author
Built for **CodeAlpha AI Internship Program**
