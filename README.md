# Online Board Game (Ticket to Ride Inspired) 🚂

*Work in Progress – BSc Thesis Project for ELTE IK Computer Science*

## About the Project
This repository contains the source code for my Computer Science thesis at Eötvös Loránd University (ELTE IK). The project aims to create a fully functional, online multiplayer version of a board game inspired by the mechanics of *Ticket to Ride*.

## Architecture & Tech Stack

### Backend (Python / FastAPI)
* **API & Business Logic:** The backend serves HTTP REST endpoints primarily routed through `main.py`.
* **Rules Engine:** A framework-independent rules module utilizing Pydantic for strict data validation and state management, structured within `core/rules.py` and `core/models.py`.
* **Map Management:** Map layouts are loaded via `core/loader.py` and stored in JSON format, such as `core/data/map_testmap1.json`.
* **Testing:** The backend logic is verified using `pytest`, with map-specific tests located in `tests/test_map.py`.

### Frontend (React / Vite)
* **User Interface:** A fast, Vite-powered React application housed in the `frontend/` directory, driven by `main.jsx`, `App.jsx`, and `Game.jsx`.
