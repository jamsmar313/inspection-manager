# Inspection Manager — Ubuntu starter prototype

This is a **development prototype**, not a production-ready hosted application. It includes company-scoped inspection records, Django admin, a read-only desktop/mobile dashboard, and a safe workbook preview command. It does **not** yet implement imports, Google Calendar synchronization, payment processing, field photo uploads, or customer signups.

## Run on Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
unzip inspection_platform_starter.zip
cd inspection_platform_starter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set a unique, secret DJANGO_SECRET_KEY
python manage.py makemigrations inspections
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ and sign in. Create a **Company**, then a **Membership** connecting your admin user to that company, then create a test Inspection. The dashboard is at http://127.0.0.1:8000/.

## Preview your existing workbook (read-only)

Copy `Working Master test.xlsx` into the project folder and run:

```bash
python manage.py preview_workbook 'Working Master test.xlsx'
```

This prints the number of records and repeated job numbers. It does not import anything, protecting existing records while we confirm duplicate rules and field mappings.

## Database and hosting

The starter defaults to **SQLite for easy local testing**. When ready for online deployment, set the POSTGRES_* variables in `.env` to use PostgreSQL. Production hosting also requires HTTPS, hardened settings, secure media storage, backups, monitoring, tenant access tests, and a review of how personal/policy information is handled. Do not put real insured information into a publicly accessible deployment yet.

## Next development milestones

1. Build validated, preview-first import with per-vendor mappings and fee preservation.
2. Add secure forms for editing jobs, scheduling, and status transitions.
3. Add Calendar OAuth and event synchronization.
4. Add mobile field notes and secure photo uploads.
5. Test cross-company isolation and deploy securely online.
