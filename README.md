# Cryton — Website

Bilingual (EN/NO) company website built with Flask. Includes a contact form backed by Brevo SMTP, case study pages, and a fully responsive dark UI.

---

## Project structure

```
cryton/
├── app.py                        # Flask app, all routes, all translation strings
├── requirements.txt
├── .env                          # Your secrets — never commit this
├── .env.example                  # Template to copy from
├── .gitignore
├── templates/
│   ├── base.html                 # Shared nav, footer, language switcher
│   ├── index.html                # Homepage (hero, services, process, portfolio)
│   ├── about.html                # About page
│   ├── contact.html              # Contact form
│   └── case_study.html           # Individual case study pages
└── static/
    ├── css/main.css              # All styles (responsive, dark theme)
    ├── js/
    │   ├── main.js               # Nav, language switcher, smooth scroll
    │   └── contact.js            # Contact form AJAX submit
    └── images/
        ├── logo-mark.svg
        ├── services/             # SVG illustrations for service cards
        └── portfolio/            # SVG diagrams for portfolio / case study pages
```

---

## Prerequisites

- Python 3.10+
- A [Brevo](https://brevo.com) account (free tier: 300 emails/day)

---

## Local setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd cryton

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file
cp .env.example .env
# Open .env and fill in your Brevo credentials (see Email setup below)

# 5. Run the development server
python app.py
# → http://localhost:5000
```

---

## Environment variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session secret — set a long random string in production |
| `MAIL_SERVER` | `smtp-relay.brevo.com` |
| `MAIL_PORT` | `587` |
| `MAIL_USERNAME` | Brevo SMTP login (e.g. `ab2f44001@smtp-brevo.com`) |
| `MAIL_PASSWORD` | Brevo SMTP key (starts with `xsmtpsib-...`) |
| `CONTACT_RECIPIENT` | Email address that receives contact form submissions |

---

## Email setup (Brevo)

### Step 1 — Get your SMTP credentials

1. Log in to [app.brevo.com](https://app.brevo.com)
2. Go to **SMTP & API** → **SMTP** tab
3. Note the **Login** value (looks like `ab2f44001@smtp-brevo.com`) — this is your `MAIL_USERNAME`
4. Under **Your SMTP Keys**, click **Generate SMTP key**, name it (e.g. `cryton`), and copy the key — this is your `MAIL_PASSWORD`

### Step 2 — Whitelist your IP address

Brevo blocks SMTP calls from unknown IPs by default.

1. In the same **SMTP & API** page, click **"Click here"** in the blue IP restriction notice
2. Add every IP that will send mail:

| Environment | IP to add |
|---|---|
| **Your laptop** | Your current public IP — find it at [api.ipify.org](https://api.ipify.org) |
| **Cloud server** | The static IP of your VPS / cloud instance |

> **Tip for cloud:** If your cloud provider assigns a static IP (AWS Elastic IP, DigitalOcean Reserved IP, etc.) add it here. If IP changes on every deploy (e.g. Railway free tier), disable the IP restriction toggle in Brevo instead.

### Step 3 — Test the connection

```bash
python -c "
from dotenv import load_dotenv; load_dotenv()
import os, smtplib
s = smtplib.SMTP(os.getenv('MAIL_SERVER'), 587)
s.starttls()
s.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
print('Connection OK — email is ready')
s.quit()
"
```

---

## Language switching

Two languages are supported out of the box: English (`en`) and Norwegian (`no`).

Switch via URL param or the nav toggle:
```
/?lang=en
/?lang=no
```

The selected language is stored in a cookie for all subsequent pages.

### Adding a new language

1. In `app.py`, add a new top-level key to `TRANSLATIONS` matching the same structure as `'en'`
2. Add a button to the language switcher in `templates/base.html`

---

## Case study pages

Case studies live at `/case-study/<slug>`. The four slugs are:

| Slug | Project |
|---|---|
| `aws-migration` | Multi-region AWS migration |
| `analytics-pipeline` | Real-time analytics pipeline |
| `zero-trust-auth` | Zero-trust auth system |
| `hr-portal` | Power Platform HR portal |

To add a new case study:
1. Add the slug to the `portfolio.list` in `TRANSLATIONS` (both `en` and `no`) with an `'img'` and `'slug'` key
2. Add a matching entry to `case_studies` in both languages with `metrics`, `tech`, `timeline`, `challenge`, `solution`, `outcome`
3. Add a portfolio SVG image to `static/images/portfolio/`

---

## Cloud deployment

### Gunicorn (any Linux VPS)

```bash
# Install
pip install gunicorn

# Run (4 workers, port 8000)
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Serve behind **Nginx** as a reverse proxy:

```nginx
server {
    listen 80;
    server_name cryton.no www.cryton.no;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Railway / Render (one-click PaaS)

Add a `Procfile` to the project root:

```
web: gunicorn app:app
```

Then set all variables from `.env` in the platform's **Environment Variables** dashboard. Do **not** upload your `.env` file — paste the values manually.

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

```bash
docker build -t cryton-web .
docker run -p 8000:8000 --env-file .env cryton-web
```

> **Brevo IP for cloud:** After deploying, find your server's public IP and add it to Brevo's authorized IP list (same steps as local setup). On platforms with dynamic IPs (Railway free tier, Render free tier), disable the IP restriction in Brevo instead.

---

## Production checklist

- [ ] `SECRET_KEY` set to a long random string (not the default)
- [ ] `.env` file is **not** committed to git
- [ ] Brevo SMTP key rotated after any accidental exposure
- [ ] Server IP whitelisted in Brevo (or IP restriction disabled)
- [ ] Nginx + SSL certificate (Let's Encrypt / Certbot)
- [ ] `DEBUG=False` — Flask debug mode off in production (`app.run(debug=False)`)
