# 🎓 TuniSci: Tunisian Scholars Research Impact Analysis

This project analyzes the research impact of Tunisian scholars ### Option 3: Quick Setup with uv Only 🚀y scraping data from Google Scholar. It includes **5945 scholars** from various universities, research fields, and interests. The goal is to reflect the real impact and contribution of Tunisian universities to global research and higher education quality.

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
- **Scholars**: 5945 Tunisian scholars from different universities and research fields.
- **Objective**: Reflect the real impact and contribution of Tunisian universities on global research and higher education quality.

---

## 📈 Significant Statistics
- **Top 100 Scholars**: [View Ranking](scholars_ranking.md)

---

## 🚀 Running the Streamlit App Locally

### Prerequisites
- [pyenv](https://github.com/pyenv/pyenv) (for Python version management)
- [uv](https://docs.astral.sh/uv/) (for fast package management and virtual environments)
- [Poetry](https://python-poetry.org/) (for dependency management)
- Docker (optional, for containerized deployment)

---

### Option 1: Complete Setup with pyenv + uv + Poetry (Recommended) 🚀
1. Clone the repository:
   ```bash
   git clone https://github.com/Frostbite22/TuniSci.git
   cd TuniSci
   ```

2. Install pyenv (if not already installed):
   ```bash
   # macOS with Homebrew
   brew install pyenv
   
   # Or using the installer
   curl https://pyenv.run | bash
   ```

3. Install and set local Python version:
   ```bash
   # Install Python 3.11 (or your preferred version)
   pyenv install 3.11.9
   
   # Set local Python version for this project
   pyenv local 3.11.9
   ```

4. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

5. Create virtual environment with uv:
   ```bash
   uv venv .venv
   
   # Activate the virtual environment
   source .venv/bin/activate
   ```

6. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

7. Configure Poetry to use the existing virtual environment:
   ```bash
   poetry config virtualenvs.prefer-active-python true
   ```

8. Install dependencies with uv:
   ```bash
   uv pip install -r requirements.txt
   ```

9. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   # Or with Poetry if you prefer
   poetry run streamlit run streamlit_app.py
   ```

10. Access the app:
    Open your browser and go to `http://localhost:8501`.

### Option 2: Quick Setup with Poetry Only 🐍
1. Clone the repository:
   ```bash
   git clone https://github.com/Frostbite22/TuniSci.git
   cd TuniSci
   ```

2. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies and create virtual environment:
   ```bash
   poetry install
   ```

4. Run the Streamlit app:
   ```bash
   poetry run streamlit run streamlit_app.py
   ```

### Option 2: Run with uv �
1. Clone the repository:
   ```bash
   git clone https://github.com/Frostbite22/TuniSci.git
   cd TuniSci
   ```

2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create virtual environment with uv:
   ```bash
   uv venv .venv
   
   # Activate the virtual environment
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

5. Run the Streamlit app:
   ```bash
   uv run streamlit run streamlit_app.py
   ```

6. Access the app:
   Open your browser and go to `http://localhost:8501`.

---

### Option 4: Run with Docker 🐳
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

4. Access the app:
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