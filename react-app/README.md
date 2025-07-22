# ReactJS Frontend for FastAPI Fraud Detection

This app provides user registration, login, and transaction fraud check using FastAPI backend.

## Pages
- Registration: `/register`
- Login: `/login`
- Fraud Check: `/fraud-check`

## Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the app:
   ```bash
   npm start
   ```

## API Endpoints
- `POST /signup` for registration
- `POST /token` for login
- `POST /predict` for fraud check (JWT required)

## Notes
- JWT token is stored in localStorage and sent in Authorization header for protected requests.
- Update API URLs if your FastAPI backend runs on a different host/port.
