# Ali Kassem — Personal Engineering Portfolio

[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v3.4.17-blue?logo=tailwind-css)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Verification Suite](https://img.shields.io/badge/Tests-92%20Passed-emerald)](test_portfolio.py)

The personal engineering portfolio of **Ali Kassem**, Computer Science student at E-JUST (Egypt-Japan University of Science and Technology) specializing in Artificial Intelligence and Data Science, Microsoft Data Engineer track trainee at DEPI, and creator of Xare AI.

---

## 🚀 Key Architecture & Featured Projects

### 1. Xare AI Platform (V2)
- **Use Case:** Multimodal AI application and orchestration platform.
- **Orchestration Layer:** 120-node n8n workflow execution graph managing state transitions, request validation, fallback error handling, and payload transformations.
- **Model Routing:** Tiered prompt routing across Gemini, Qwen, GPT-OSS, Whisper, and Deepgram.
- **Voice Streaming:** Real-time bidirectional voice streaming over WebSockets.
- **Client Cache:** React/TypeScript interface using IndexedDB for client-side audio/image media persistence.
- **Live Demo:** [https://xare-ai.vercel.app](https://xare-ai.vercel.app)

### 2. Supply Chain Management (SCM) Simulation
- **Use Case:** Discrete-event enterprise supply chain simulation.
- **Architecture:** Object-Oriented Programming (OOP) in Python with modular domain models and the Proxy design pattern.
- **Persistence:** SQLite relational database with transactional integrity.
- **Local AI:** Integrated offline local LLM pipeline for customer review sentiment analysis and dynamic marketing copy generation.
- **Repository:** [https://github.com/Ali-Kassem-AK/SCM-Simulation-Project/](https://github.com/Ali-Kassem-AK/SCM-Simulation-Project/)

---

## 🛠️ Tech Stack & Implementation Details

- **Frontend:** Semantic HTML5, Vanilla JavaScript, SVG symbol sprite.
- **Styling:** Tailwind CSS v3.4.17 with custom engineering design tokens, accessible focus states, and reduced-motion support.
- **SEO & Metadata:** OpenGraph tags, Twitter Card tags, and Schema.org `Person` JSON-LD structured data.
- **Internationalization:** Dynamic client-side localization for English (`en`), Arabic (`ar`, with automatic RTL adjustment), and Japanese (`ja`).

---

## 💻 Local Development & Build Commands

### Prerequisites
- Node.js (v18+ recommended)
- Python 3.10+ (for verification test suite)

### Build CSS
To compile Tailwind CSS:
```bash
npx tailwindcss -i ./input.css -o ./style.css --minify
```
Or with npm:
```bash
npm run build
```

### Run Verification Tests
To run the automated 92-check verification suite (verifying HTML, accessibility, links, metadata, assets, and build integrity):
```bash
python test_portfolio.py
```
Or:
```bash
npm test
```

### Preview Locally
You can serve the directory using any static file server:
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your web browser.

---

## 📬 Contact Information

- **Email:** [ali.kassem.contact@gmail.com](mailto:ali.kassem.contact@gmail.com)
- **LinkedIn:** [linkedin.com/in/aliahmedkassem](https://www.linkedin.com/in/aliahmedkassem/)
- **GitHub:** [github.com/Ali-Kassem-AK](https://github.com/Ali-Kassem-AK)
- **Location:** Alexandria, Egypt • E-JUST University
