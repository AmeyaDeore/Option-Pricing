# Option-Pricing and 3D Volatility Surface Analytics

This repository contains tools and applications for option pricing and options analytics. It builds upon foundational quantitative models by introducing a modern, full-stack, institutional-grade 3D Options Analytics Surface application.

## Acknowledgments

This repository is a fork. The directories and notebooks concerning European Options, Exotics, and basic Implied Volatility calculations are the work of the original repository author. The 3D Options Analytics Surface application (located in the `iv-surface-project` directory) was independently developed and implemented in this fork.

## 3D Options Analytics Surface Application (`iv-surface-project`)

This module features a high-performance, containerized full-stack application designed to extract market-implied volatility and the Greeks from live option chains, visualizing them as interactive 3D surfaces.

### Features Implemented

* **Vectorized Mathematics Engine**: Utilizes NumPy for high-speed, parallel calculation of the Black-Scholes-Merton equations and the Newton-Raphson root-finding algorithm.
* **Advanced Financial Rigor**: Integrates dynamic 10-Year Treasury Yields (risk-free rate) and continuous dividend yields through the yfinance API for precise institutional-grade pricing.
* **Comprehensive Greeks Calculation**: Natively derives first and second-order partial derivatives, including Delta, Gamma, Theta, Vega, and Rho.
* **Interactive 3D Visualization**: A Streamlit frontend powered by Plotly allows users to dynamically swap the Z-axis to visualize Implied Volatility or any of the calculated Greeks.
* **Robust Caching Architecture**: Implements local frontend caching and an in-memory Time-To-Live (TTL) cache in the FastAPI backend to ensure rate-limiting compliance and rapid dashboard rendering.
* **DevOps and Containerization**: Fully containerized using Docker and Docker Compose for seamless environment consistency and scalable deployment.

### How to Run the Application

#### Prerequisites
* Docker and Docker Compose installed on your system.

#### Running with Docker
1. Navigate to the application directory:
   ```bash
   cd iv-surface-project
   ```
2. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Access the application interfaces:
   * **Streamlit Frontend (UI)**: http://localhost:8501
   * **FastAPI Backend (API Documentation)**: http://localhost:8000/docs

#### Running Locally (Without Docker)
1. Navigate to the application directory:
   ```bash
   cd iv-surface-project
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # On Windows use: venv\Scripts\activate
   # On macOS/Linux use: source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Start the FastAPI backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. Start the Streamlit frontend in a new terminal window:
   ```bash
   streamlit run app.py
   ```

---

## Original Repository Contents

The following modules were developed by the original repository author.

### European Options

This folder contains notebooks with for the pricing of European options with the following models:

- Black-Scholes,
- Merton jump diffusion.

#### Black-Scholes

Pricing of European options according to the Black-Scholes model using the following methods:

- Analytical solution,
- Monte Carlo,
- Finite difference (explicit scheme),
- Fourier transform.

#### Merton Jump Diffusion

Pricing of European options according to the Merton jump diffusion model using the following methods:

- Analytical solution,
- Monte Carlo,
- Fourier transform.

#### Heston model

Pricing of European options according to the Heston stochastic volatility model using the following methods:

- Analytical solution
- Monte Carlo

#### Binomial model

Pricing of European options according to the binomial model (Cox, Ross, Rubinstein).

### Exotics

Pricing of the following exotic options:

- Barrier (discrete and continuous monitoring, analytical and Monte Carlo).

#### Barrier options

Pricing of barrier options (discretely and continuously monitored) using the following methods:

- Analytical solution,
- Monte Carlo.

### Implied Volatility

Computation of implied volatility for European options using the Newton-Raphson method and the Black-Scholes model. Plotting of the volatility smile.
