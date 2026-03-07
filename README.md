
# GEMHUB_BACKEND

This is the backend project for Gem Hub.

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/NeoArkByte/gem-hub-backend

cd gem-hub-backend
````

2. **Install uv package manager** (if not installed)

```bash
pip install uv
```

3. **Create and activate virtual environment**

```bash
uv venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

4. **Install dependencies**

```bash
uv sync
```

5. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Start the development server**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to confirm the server is running.


