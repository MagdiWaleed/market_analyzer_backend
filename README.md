# Market Analyzer Agent – Backend

A **backend service** for the Market Analyzer Agent that generates detailed market reports. It analyzes user-desired product against competitors’ offerings in the Saudi Arabian market and produces actionable insights, including:

* Gaps and weaknesses in the market
* Recommendations for improvement
* Competitor product reports and overall company analysis

> 🔍 Powered by **LangChain, LangGraph**, and **Flask** for scalable, multi-step AI workflows.

---

## ✨ Features

* Multi-step reasoning with **LangGraph orchestration**
* Contextual market insights and up-to-date informations about the companies using [**LangChain Community**](https://www.langchain.com/community) especially [**Tavily Search Tool**](https://python.langchain.com/docs/integrations/tools/tavily_search/)
* Returns structured reports with recommendations and competitor analysis

---

## ⚙️ Installation

Clone the backend repo:

```bash
git clone https://github.com/MagdiWaleed/market_analyzer_backend.git
cd market-analyzer-backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend API:

```bash
python run.py
```

---

## 🛠 Tech Stack

* **AI Orchestration** → LangGraph, LangChain
* **Backend** → Flask REST API
* **Language** → Python
* **Region Focus** → Saudi Arabia Market
* **Frontend** → Streamlit (frontend)

---

## 📂 Project Structure

```
.
├── app.py                  # Flask backend API
├── agents/                 # LangGraph agent orchestration
├── data/                   # Market and competitor datasets
├── reports/                # Generated report templates and outputs
├── requirements.txt
└── README.md
```

---

## 🚀 Future Improvements

* Expand to other regional markets
* Add user authentication and profiles
* Integrate dynamic real-time product data sources
* Dockerize backend for cloud deployment

---

## 📬 Contact

If you find this project useful, feel free to ⭐ star the repo and connect on [LinkedIn](www.linkedin.com/in/magdi-waleed).
