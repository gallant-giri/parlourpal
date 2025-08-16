# ParlorPal - AI-Powered Marketing Automation Platform

## Project Overview

ParlorPal is a comprehensive Django-based web application that leverages multiple AI services to provide automated marketing solutions for small businesses, particularly beauty parlors and local service providers. The platform integrates Google Vertex AI, Cohere, and Google Gemini to generate promotional content, manage business profiles, and automate customer engagement through festival notifications.

## Architecture & Technical Implementation

### Core Technologies


# ParlorPal

<div align="center">
	<img src="https://raw.githubusercontent.com/gallant-giri/parlorpal/main/static/images/HomePageParlourpal.png" alt="ParlorPal Dashboard" width="320" />
</div>

**AI-powered marketing automation for small businesses.**

---

## 🚀 Technologies Used

**Backend:** Django 5.1  
**Database:** SQLite3 (PostgreSQL-ready)  
**AI Services:** Google Vertex AI (Imagen), Cohere, Google Gemini  
**Image Processing:** Pillow, Cloudinary  
**Email:** Gmail SMTP  
**Static Files:** WhiteNoise  
**Environment:** python-dotenv  
**Deployment:** Gunicorn, Railway

## 🧩 Main Features

- **AI Poster Generation:** Google Vertex AI Imagen for custom promotional posters
- **AI Text Generation:** Cohere for captions and marketing content
- **Chatbot Assistant:** Google Gemini for business advice
- **Business Profile Management:** Custom user model, logo upload, Cloudinary integration
- **Festival Notifications:** Automated email reminders for events
- **User Activity Tracking:** Search history, analytics, insights
- **Mobile-Responsive UI:** Bootstrap-based, optimized for all devices

## 🗂️ Core Models

```python
CustomUser(AbstractUser)   # User with email verification
BusinessProfile           # Business info & branding
SearchHistory             # User search queries
PosterGeneration          # AI-generated posters
Festival                  # Festival notifications
UserHistory               # Activity tracking
```

## 🔗 Key Endpoints

```
/login/             # User login
/register/          # Registration & business profile
/dashboard/         # Main dashboard
/ai/                # AI text generation
/generate_poster/   # Poster generation
/chatbot/           # Chatbot assistant
/profile/           # Profile management
/history/           # Activity tracking
/insights/          # Analytics
/verify-email/<token>/     # Email verification
/toggle-notifications/     # Festival notifications
```

## ⚙️ Environment Variables

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

## 🛠️ Management Commands

```bash
python manage.py send_festival_notifications
python manage.py cleanup_orphaned_data
python manage.py create_missing_profiles
```

## 🏆 Highlights

- Multi-AI integration (Vertex AI, Cohere, Gemini)
- Cloudinary for image storage & optimization
- Automated email system (verification, notifications)
- Custom user authentication with email verification
- Responsive, modern UI for technical and non-technical users

---

<div align="center">
	<b>Made for Epsilon Hackathon 2025</b><br>
	<i>Team HustlePioneers</i>
</div>
/history/           # User activity tracking
