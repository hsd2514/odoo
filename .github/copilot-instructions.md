## 🤖 Using Copilot in This Monorepo

This project is designed for rapid, beginner-friendly hackathon development. To get the best results from GitHub Copilot, follow these detailed instructions:

- **Backend (FastAPI):**
  - Always use routers (`from fastapi import APIRouter`) for endpoints. Place each logical group of endpoints in its own file under `app/routers/`.
  - Keep code modular: use separate files for models, schemas, routers, and business logic.
  - Keep files as small and focused as possible. Avoid putting too many endpoints or models in a single file.
  - Use clear docstrings and type hints for all functions and classes.
  - Add comments and examples for beginners.
  - Follow the structure and tips in `backend/app/README.md`.

- **Frontend (React + Tailwind + DaisyUI):**
  - Always use DaisyUI components for UI (buttons, cards, forms, etc.) for a consistent look.
  - Use Tailwind utility classes for layout and spacing.
  - Write modular React code and keep components as small and focused as possible.
  - Keep React components simple and functional.
  - Use `npm` for package management.

- **General:**
  - Write code and documentation that is easy for beginners to understand.
  - Avoid advanced patterns unless necessary for the hackathon.
  - Keep `.vscode` and `.github` folders in the repo for team productivity.
  - Refer to the main project README and backend/app/README.md for feature lists, API endpoints, and project structure.

**Example Copilot Prompts:**

- "Add a new API route to app/routers/skills.py for listing all skills."
- "Create a DaisyUI card component for displaying a user profile."
- "Write a Pydantic schema for the feedback model."

By following these instructions, Copilot will generate code that matches the team's standards and is easy for everyone to understand and extend.
<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->


# Monorepo Coding Instructions

## General
- This is a monorepo with a FastAPI backend and a React + Tailwind CSS + DaisyUI frontend.
- Keep backend and frontend code strictly separated in their respective folders.
- Use clear, beginner-friendly code and comments where possible.
- Follow best practices for both Python and JavaScript/React code.

## Backend (FastAPI)
- All backend code lives in the `backend/` folder.
- Use a single `main.py` as the entry point for beginners.
- Use `requirements.txt` for dependencies.
- For larger apps, always use FastAPI routers (`from fastapi import APIRouter`) to organize endpoints in separate modules (e.g., `routers/`).
- Write modular code and keep files as small and focused as possible.
- Use clear docstrings and type hints.

## Frontend (React + Tailwind + DaisyUI)
- All frontend code lives in the `frontend/` folder.
- Always use DaisyUI components for UI (buttons, cards, forms, etc.) for a consistent look.
- Use Tailwind utility classes for layout and spacing.
- Write modular React code and keep components as small and focused as possible.
- Keep React components simple and functional.
- Use `npm` for package management.

## Collaboration
- Write code and documentation that is easy for beginners to understand.
- Add comments and examples where helpful.
- Avoid advanced patterns unless necessary for the hackathon.

## VS Code
- Keep `.vscode` and `.github` folders in the repo for team productivity.

## Example: Add a new API route
```python
# In backend/main.py
@app.get("/hello")
def say_hello():
    return {"message": "Hello, world!"}
```

## Example: Add a new DaisyUI button
```jsx
<button className="btn btn-secondary">Click Me</button>
```
