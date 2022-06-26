<div align="center">
  <a href="#">
    <img
      alt="Portfolio Tracker Logo"
      src="https://raw.githubusercontent.com/Jeevan-J/binance-portfolio-tracker/main/app/assets/PortfolioTrackerLogos/Portfolio%20Tracker%20Rectangle.png"
      width="500"
    />
  </a>
  <h1>Binance Portfolio Tracker</h1>
  <p>
    <strong>Open Source Binance Portfolio Tracker</strong>
  </p>
  <p>
    <a href="#contributing">
      <img src="https://img.shields.io/badge/contributions-welcome-orange.svg"/></a>
    <a href="https://github.com/Jeevan-J/binance-portfolio-tracker/actions/workflows/docker-publish.yml" rel="nofollow">
      <img src="https://github.com/Jeevan-J/binance-portfolio-tracker/actions/workflows/docker-publish.yml/badge.svg" alt="Build Status"/></a>
    <a href="https://opensource.org/licenses/MIT" rel="nofollow">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
  </p>
  <h1></h1>
</div>

**Binance Portfolio Tracker** is an open source tracking and visualization application built with web technology. The application empowers busy people to keep track of their cryptocurrencies and make solid, data-driven investment decisions.

## Why Binance Portfolio Tracker?

Binance Portfolio Tracker is for you if you are...

- 💼 investing cryptocurrencies on binance platform
- 🏦 pursuing a buy & hold strategy
- 🎯 interested in getting insights of your portfolio composition
- 👻 valuing privacy and data ownership
- 🧘 into minimalism
- 🧺 caring about diversifying your financial resources
- 🆓 interested in financial independence
- 🙅 saying no to spreadsheets in 2022
- 😎 still reading this list

## Features

- ✅ Create, update and delete investment pairs
- ✅ Various charts
- ✅ Static analysis to identify potential risks in your portfolio
- ✅ Import and export transactions

## Technology Stack

Binance Portfolio Tracker is a web application written in [Ploty Dash](https://plotly.com/dash/).

### Backend

The backend is based on [Python](https://python.org) using [SQLite3](https://www.sqlite.org) as a database.

### Frontend

The frontend is built with [Ploty Dash](https://plotly.com/dash/) with utility classes from [Bootstrap](https://getbootstrap.com) and callbacks written in [Python](https://python.org).

## Self-hosting

### Run with Docker Compose

#### Prerequisites

- Basic knowledge of Docker
- Installation of [Docker](https://www.docker.com/products/docker-desktop)
- Local copy of this Git repository (clone)
- You need to set your binance API keys (read-only) in `.env` as follows or pass them to the docker environment using `-e` flag.
  
  ```bash
    ENVIRONMENT=<PROD-or-TEST>
    BINANCE_PROD_API_KEY=<BINANCE-PROD-API-KEY>
    BINANCE_PROD_API_SECRET_KEY=<BINANCE-PROD-API-SECRET-KEY>
    BINANCE_TEST_API_KEY=<BINANCE-TEST-API-KEY>
    BINANCE_TEST_API_SECRET_KEY=<BINANCE-TEST-API-SECRET-KEY>
  ```

#### a. Run environment

Run the following command to start the Docker images from [Docker Hub](https://hub.docker.com/repository/docker/jeevanj/binance-portfolio-tracker):

```bash
docker-compose --env-file ./.env -f docker/docker-compose.yml up -d
```

#### b. Build and run environment

Run the following commands to build and start the Docker images:

```bash
docker-compose --env-file ./.env -f docker/docker-compose.build.yml build
docker-compose --env-file ./.env -f docker/docker-compose.build.yml up -d
```

## Development

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Python](https://python.org) (version >= 3.8+ and <3.10)
- A local copy of this Git repository (clone)

### Setup

1. Install virtual environment | `python -m pip install virtualenv`
2. Create a virtual environment | `python -m virtualenv pt_env`
3. Activate the virtual environment 
   - Windows - `pt_env\Scripts\activate`
   - Linux - `source pt_env/bin/activate`
4. Install python packages | `pip install -r requirements.txt`

### Start Server
Go to application directory
<ol type="a">
  <li>Debug: Run <code>python dashboard.py</code></li>
  <li>Serve: Run <code>gunicorn -b 0.0.0.0:8000 dashboard:server</code></li>
</ol>

## Contributing

Binance Portfolio Tracker is **100% free** and **open source**. We encourage and support an active and healthy community that accepts contributions from the public - including you.

## License

© 2022 [Binance Portfolio Tracker](#)

Licensed under the [MIT License](https://opensource.org/licenses/MIT)