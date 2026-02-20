# 📦 SQLAlchemy + SQLite Boilerplate

[![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python)](https://www.python.org/downloads/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-orange?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/actions/workflows/tests.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/actions)

> A minimal, opinionated starter kit for building Python applications that persist data with **SQLAlchemy** and **SQLite**.  
> It includes model definitions, a session factory, migrations via **Alembic**, and a few handy scripts for common CRUD operations.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Quick Usage Example](#quick-usage-example)
- [Running the Test Suite](#running-the-test-suite)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- ⚡ **SQLAlchemy 2.x** core & ORM
- 🗄️ **SQLite** as a zero‑config, file‑based DB (perfect for prototypes & small apps)
- 🔧 Centralised `Session` factory (`db.session`) with context‑manager support
- 📦 **Alembic** migrations (auto‑generated + manual migration scripts)
- 🧪 Ready‑to‑run **pytest** suite (example tests for models & CRUD)
- 🐳 Optional **Docker**/Docker‑Compose setup for reproducible environments
- 📚 Well‑documented code snippets and helper utilities

---

## Prerequisites

| Tool | Minimum version |
|------|-----------------|
| Python | 3.9 |
| pip | latest (≥ 23) |
| Git | any recent version |
| (Optional) Docker & Docker‑Compose | 20.10+ / 2.0+ |

> **Tip:** If you work on multiple Python projects, consider using `pyenv` + `virtualenv` or `conda` to keep environments isolated.

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
cd <YOUR_REPO>

# 2. Create a virtual environment (recommended)
python -m venv .venv
# Activate (Linux/macOS)
source .venv/bin/activate
# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -U pip setuptools wheel
pip install -r requirements.txt

# 4. Install the editable package (if you have a setup.cfg / pyproject.toml)
pip install -e .
