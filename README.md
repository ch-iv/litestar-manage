# litestar-manage
litestar-manage is a project scaffolding tool for Litestar. It allows the user to quickly create a starter Litestar
project using a CLI.

## Usage
To quickly create a starter project, run the following:
```
litestar-manage init --app-name MyProject
```
This will initialize a Litestar project named MyProject in the current working directory. The project has the following
file tree structure:
```
app/
├─ templates/
│  ├─ index.html
├─ controllers/
│  ├─ __init__.py
│  ├─ web.py
├─ tests/
│  ├─ __init__.py
├─ assets/
├─ __init__.py
├─ app.py
├─ config.py
.gitignore
README.md
```