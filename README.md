# ⚡ Nexus: Context-Aware Collaborative Learning
**Vashisht Hackathon 3.0 Submission | Track: EdTech**

![Streamlit](https://img.shields.io/badge/Deployed_on-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Powered_by-Gemini_2.5_Flash-8E75B2?style=for-the-badge)

---

## 🚀 Live Links & Demo
* **Live Web App:** https://nexus-vashisht-edtech.streamlit.app
* **Demo Video:** https://drive.google.com/file/d/1d05OMgsTTee0KZJQVUEL6GrCgHun1MCM/view?usp=sharing

---

## 📌 The Problem
Students often take unstructured, context-dependent notes during fast-paced lectures. This leads to inefficient revision, where learners spend more time re-learning than reinforcing concepts. Simultaneously, peer learning remains underutilized due to social hesitation, lack of suitable partners, and the absence of structured collaboration systems. This disconnect results in poor knowledge retention and increased academic stress. 

## 💡 Our Solution: Nexus
Nexus is an AI-powered EdTech ecosystem designed to provide the missing unified approach that bridges personal understanding with peer interaction. 

### Core Features
* **🧠 Solo Study Engine:** Utilizes Google's Gemini Vision API to instantly transcribe messy, handwritten notes and convert them into structured Study Guides, interactive Q&A modules, and downloadable PowerPoint decks.
* **🔒 Secure Peer Hubs:** Private, code-locked workspaces where study groups can pool their raw notes together. The AI synthesizes these diverse contributions into a single, comprehensive Master Guide.
* **🎯 Algorithmic Peer Matchmaking:** Analyzes student strengths and weaknesses to intelligently pair peers for targeted tutoring, overcoming traditional social hesitation.
* **⏱️ Integrated Productivity:** Features a built-in Pomodoro Focus Room and a Gamified "Contribution XP" tracker to keep learners engaged and motivated.

---

## 📊 Evaluation Criteria Mapping

### 1. Innovation 
While most EdTech tools focus solely on flashcards from digital text, Nexus solves the "cold start" problem of studying by parsing **handwritten notes** via Vision AI. Furthermore, it introduces the novel concept of **AI-Synthesized Peer Collaboration**—taking multiple students' messy notes on the same topic and merging them into one master study guide.

### 2. Technical Implementation 
* **Robust AI Pipeline:** Seamlessly chains Gemini 2.5 Flash prompts to handle OCR transcription, strict JSON-formatting for data extraction, and dynamic slide generation.
* **Dynamic Smart Pagination:** A custom chunking algorithm ensures that auto-generated PowerPoint slides gracefully overflow to new slides if character counts exceed safe limits, handling edge cases gracefully.
* **Stateless Database Architecture:** Utilizes a custom local JSON document store capable of handling real-time chat, profile updates, and secure hub data without heavy external database overhead.

### 3. Feasibility
Nexus is highly practical for real-world campus scenarios. It requires zero onboarding friction—students simply snap a picture of their notebook to receive instant value. The platform features dynamic, user-generated subject additions, ensuring it can scale to fit any university course catalog effortlessly. 

---

## ⚙️ Setup Instructions
*Note: This application requires an active internet connection to communicate with the Gemini API.*

**1. Clone this repository:**
bash
git clone [https://github.com/yashvantatk/nexus-learning.git](https://github.com/yashvantatk/nexus-learning.git)
cd nexus-learning

**2. Install dependencies:**
Bash
pip install -r requirements.txt

**3. Set up your environment variables:**
Create a .env file in the root directory and add your Gemini API Key:

Code snippet
GEMINI_API_KEY="your_api_key_here"

**4. Run the application:**

Bash
streamlit run app.py

🛠️ Tech Stack Disclosures

Frontend & Framework: Streamlit, HTML/JS Components

AI/LLM: Google GenAI SDK (Gemini 2.5 Flash)

Data Storage: Custom JSON Document Store (db_engine.py)

Export Libraries: python-pptx, fpdf, python-docx, Pillow

---

