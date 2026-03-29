# ⚡ Nexus: Context-Aware Collaborative Learning
**Vashisht Hackathon 3.0 Submission | Track: EdTech**

![Streamlit](https://img.shields.io/badge/Deployed_on-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Powered_by-Gemini_2.5_Flash-8E75B2?style=for-the-badge)

---

## 🚀 Live Links & Demo
* **Live Web App:** [Insert your Streamlit Share link here]
* **Demo Video:** [Insert your YouTube/Drive link here]

---

## 📌 The Problem
[cite_start]Students often take unstructured, context-dependent notes during fast-paced lectures[cite: 5]. [cite_start]This leads to inefficient revision, where learners spend more time re-learning than reinforcing concepts[cite: 6]. [cite_start]Simultaneously, peer learning remains underutilized due to social hesitation, lack of suitable partners, and the absence of structured collaboration systems[cite: 7]. [cite_start]This disconnect results in poor knowledge retention and increased academic stress[cite: 8]. 

## 💡 Our Solution: Nexus
[cite_start]Nexus is an AI-powered EdTech ecosystem designed to provide the missing unified approach that bridges personal understanding with peer interaction[cite: 9]. 

### Core Features
* **🧠 Solo Study Engine:** Utilizes Google's Gemini Vision API to instantly transcribe messy, handwritten notes and convert them into structured Study Guides, interactive Q&A modules, and downloadable PowerPoint decks.
* **🔒 Secure Peer Hubs:** Private, code-locked workspaces where study groups can pool their raw notes together. The AI synthesizes these diverse contributions into a single, comprehensive Master Guide.
* [cite_start]**🎯 Algorithmic Peer Matchmaking:** Analyzes student strengths and weaknesses to intelligently pair peers for targeted tutoring, overcoming traditional social hesitation[cite: 7].
* **⏱️ Integrated Productivity:** Features a built-in Pomodoro Focus Room and a Gamified "Contribution XP" tracker to keep learners engaged and motivated.

---

## 📊 Evaluation Criteria Mapping

### 1. Innovation (20%)
[cite_start]While most EdTech tools focus solely on flashcards from digital text, Nexus solves the "cold start" problem of studying by parsing **handwritten notes** via Vision AI[cite: 76, 78]. Furthermore, it introduces the novel concept of **AI-Synthesized Peer Collaboration**—taking multiple students' messy notes on the same topic and merging them into one master study guide.

### 2. Technical Implementation (35%)
* [cite_start]**Robust AI Pipeline:** Seamlessly chains Gemini 2.5 Flash prompts to handle OCR transcription, strict JSON-formatting for data extraction, and dynamic slide generation[cite: 81].
* [cite_start]**Dynamic Smart Pagination:** A custom chunking algorithm ensures that auto-generated PowerPoint slides gracefully overflow to new slides if character counts exceed safe limits, handling edge cases gracefully[cite: 83].
* [cite_start]**Stateless Database Architecture:** Utilizes a custom local JSON document store capable of handling real-time chat, profile updates, and secure hub data without heavy external database overhead[cite: 82].

### 3. Feasibility (20%)
[cite_start]Nexus is highly practical for real-world campus scenarios[cite: 85]. It requires zero onboarding friction—students simply snap a picture of their notebook to receive instant value. [cite_start]The platform features dynamic, user-generated subject additions, ensuring it can scale to fit any university course catalog effortlessly[cite: 85]. 

---

## ⚙️ Setup Instructions
*Note: This application requires an active internet connection to communicate with the Gemini API.*

**1. Clone this repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/nexus-learning.git](https://github.com/YOUR_USERNAME/nexus-learning.git)
cd nexus-learning
2. Install dependencies:

Bash
pip install -r requirements.txt
3. Set up your environment variables:
Create a .env file in the root directory and add your Gemini API Key:

Code snippet
GEMINI_API_KEY="your_api_key_here"
4. Run the application:

Bash
streamlit run app.py
🛠️ Tech Stack Disclosures
Frontend & Framework: Streamlit, HTML/JS Components

AI/LLM: Google GenAI SDK (Gemini 2.5 Flash)

Data Storage: Custom JSON Document Store (db_engine.py)

Export Libraries: python-pptx, fpdf, python-docx, Pillow
