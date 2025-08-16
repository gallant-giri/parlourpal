
# ParlorPal

AI-powered marketing automation for small businesses.

---

## 🚀 Tech Stack

- **Backend:** Django 5.1
- **Database:** SQLite3 (PostgreSQL-ready)
- **AI Services:** Google Vertex AI (Imagen), Cohere, Google Gemini
- **Image Processing:** Pillow, Cloudinary
- **Email:** Gmail SMTP
- **Static Files:** WhiteNoise
- **Environment:** python-dotenv
- **Deployment:** Gunicorn, Railway

## ⚡ Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
```

Set environment variables in a `.env` file:

```env
COHERE_API_KEY=...
GEMINI_API_KEY=...
GOOGLE_VERTEX_API_KEY=...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
GMAIL_USER=...
GMAIL_APP_PASSWORD=...
SECRET_KEY=...
DEBUG=True/False
```

## ✨ Features

- AI poster generation (Vertex AI Imagen)
- AI text/caption generation (Cohere)
- Chatbot assistant (Gemini)
- Business profile management (custom user, logo upload, Cloudinary)
- Festival notification emails
- User activity tracking & analytics
- Mobile-responsive UI (Bootstrap)

---

<div align="center">
	<b>Made for Epsilon Hackathon 2025</b><br>
	<i>Team HustlePioneers</i>
</div>
