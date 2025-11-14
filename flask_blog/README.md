# Flask Blog
- Modular blogging plataform built with Flask, designed for scalable deployment.

![Python](https://img.shields.io/badge/python-3.13.7-blue) ![Flask](https://img.shields.io/badge/flask-3.1.2-green)

## Overview
- Designed as a general purpose blog web plataform, Flask Blog demostrates a blueprint-based architecture with reusable templates and responsive UI.

## Features
- Blueprint-based modular architecture.
- Responsive UI with Bootstrap 5.
- Template inheritance for maintainable layout.
- Multi-tenat authentication via login page and registration.
- SQLAlchemy ORM integration.

## Tech Stack
| Backend -> Flask, Jinja2, SQLAlchemy |
| Frontennd -> Bootstrap 5, HTML5, CSS3 |
| Logic -> Flask-Login |

## Installation
```bash
git clone https://github.com/lazaroakiro-dev/flask_blog.git
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\Activate      # Windows
pip install -r requirements.txt
flask run
```

## Screenshots
![Screenshot](docs/images/image1.png)
- A simple UI straightfoward login page.
![Screenshot](docs/images/image2.png)
- Feed you can only see when authenticated, then you can interact.
![Screenshot](docs/images/image3.png)
- The register page, where the users input their credentials.

## Project Structure
flask_blog/
|-- app/
|   |-- about/
|   |-- auth/
|   |-- contact/
|   |-- helpers/
|   |-- main/
|   |-- models/
|   |-- services/
|   |-- static/
|   |-- templates/
|   |-- __init__.py
|   |-- extensions.py
|
|-- config.py
|-- requirements.txt
|-- run.py

## License
- MIT License © 2025 Lazaro

## Contact
Created by Lazaro - lazaro.especialista@gmail.com