# DAY1 HANDOVER
Owner: Member A — Ramesh Rao
Date: 2025-11-07

What I completed:
- Repo initialized; main contains safe Flask app.
- seed_db.py executed; app.db seeded with admin/admin123.
- templates/login.html present and app runs locally at http://127.0.0.1:5000

How to run (exact):
1. git clone <repo_url>
2. python -m venv venv
3. .\venv\Scripts\activate
4. pip install -r requirements.txt
5. python seed_db.py
6. python app.py

Notes for Day2 (Member B):
- Checkout branch: git checkout vulnerable
- Replace safe DB check with insecure string-concat query in login route.
- Restart server and test payloads: admin' OR '1'='1'--  (capture screenshots & console logs)
- Save evidence in evidence/day2/

Evidence included:
- evidence/day1/repo_branches.png
- evidence/day1/login_page.png
- evidence/day1/login_success.png
- evidence/day1/seed_db_output.png

Contact: @RameshRao
