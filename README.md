# litestar-manage

litestar-manage is a project scaffolding tool for Litestar. It allows the user to quickly create a starter Litestar
project using the Litestar CLI.

## Usage

When the litestar-manage module is installed, it will extend the Litestar native CLI. To create a starter project, run the following command:

```
litestar project init --app-name MyProject
```

This command is used to initialize a Litestar project named MyProject in the current working directory. MyProject will have the following tree structure:

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

To initialize a virtual environment with pip, `--venv pip` can be added to the init command.
