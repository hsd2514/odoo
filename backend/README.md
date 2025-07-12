# How to run the FastAPI backend

1. Open a terminal and navigate to the backend folder:
   cd backend

2. (Recommended) Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux

4. Install dependencies:
   pip install -r requirements.txt

5. Start the server:
   uvicorn main:app --reload

6. Open http://127.0.0.1:8000 in your browser.

7. For API docs, visit http://127.0.0.1:8000/docs
