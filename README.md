# 🎓 TuniSci: Tunisian Scholars Research Impact Analysis

This project analyzes the research impact of Tunisian scholars by scraping data from Google Scholar. It includes **2130 scholars** from various universities, research fields, and interests. The goal is to reflect the real impact and contribution of Tunisian universities to global research and higher education quality.

---

## 📊 Key Metrics
- **Average h-index**: **8.2**
- **What is a Good h-Index?**  
  According to Hirsch:
  - **20**: Good after 20 years of research
  - **40**: Outstanding
  - **60**: Truly exceptional

---

## 🌍 Project Scope
- **Data Source**: Google Scholar
- **Scholars**: 2130 Tunisian scholars from different universities and research fields.
- **Objective**: Reflect the real impact and contribution of Tunisian universities on global research and higher education quality.

---

## 📈 Significant Statistics
- **Average h-index**: 8.2
- **Top 100 Scholars**: [View Ranking](scholars_ranking.md)

---

## 🚀 Running the Streamlit App Locally

### Prerequisites
- Python 3.9 or higher
- Docker (optional, for containerized deployment)

---

### Option 1: Run with Python 🐍
1. Clone the repository:
   ```bash
   git clone https://github.com/Frostbite22/TuniSci.git
   cd TuniSci
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Access to the app:
   Open your browser and go to `http://localhost:8501`.

---

### Option 2: Run with Docker 🐳
1. Clone the repository:
   ```bash
   git clone https://github.com/Frostbite22/TuniSci.git
   cd TuniSci
   ```

2. Build and run the Docker container:
   ```bash
   sudo docker-compose up -d --build
   ```

3. Check the logs to confirm the app is running:
   ```bash
   sudo docker-compose logs -f
   ```

4. Access to the app:
   Open your browser and navigate to the network URL returned by the previous command.

5. To stop the container:
   ```bash
   sudo docker-compose down
   ```

---

## 🌐 Deployment
The project is deployed and accessible at:  
👉 [https://tunisci.streamlit.app/](https://tunisci.streamlit.app/)

---

## 🔮 Future Enhancements (Contributions Welcome! 🙌)
- **Average h-index by research field**: Identify the most successful fields.
- **Standard deviation of h-index**: Analyze the distribution of h-index scores (many scholars have zero publications).
- **Number of scholars per research field**: Visualize the distribution of scholars across fields.

---

## 🏆 Top 100 Scholars Ranking
Check out the ranking of the top 100 scholars:  
[View Top 100 Scholars](scholars_ranking.md)

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

