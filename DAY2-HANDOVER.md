DAY2 HANDOVER

Owner: Member B — Hiral Dinesh
Date: 2025-11-09
Branch: member-b-vulnerable
Commit: 3f0d0ea

What I completed:
-  Created intentionally vulnerable PoC login route in app.py that interpolates user input 
   into SQL (targets password_hash column) for SQL Injection demo.
-  Added/verified templates/login.html (minimal form).
-  Added seed_db.py (re-seed safe admin row) and dump_db.py (DB inspector).
-  Executed seed script and confirmed app.db contains admin user.
-  Collected evidence: server logs, payload list, HAR placeholder, and screenshots (saved to evidence/).
Note: this is a local-only lab (do not run these steps on public systems).

How to run(exact):
# 1. go to your project folder
cd "C:\Users\hiral\OneDrive\Desktop\CCN project\ccn-mini-project"

# 2. switch to the Day2 branch (we're not merging anything)
git fetch origin
git checkout member-b-vulnerable

# 3. create & activate venv (PowerShell)
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

# 4. install dependencies
python -m pip install --upgrade pip
python -m pip install Flask

# 5. seed the DB (idempotent)
python seed_db.py

# 6. quick DB check (optional)
python dump_db.py

# 7. make evidence folder and run server while saving logs
mkdir .\evidence
python app.py 2>&1 | Tee-Object -FilePath .\evidence\server_console.log
# then run tests in browser at http://127.0.0.1:5000/login

PoC exploit (exact payloads used):
- Username: admin
- Password payloads (use one at a time in the password field):
 ' OR '1'='1' --
 ' OR 1=1;--

Expected behavior: server returns Login success and terminal prints the executed SQL line:
- EXECUTED QUERY: SELECT * FROM users WHERE username = 'admin' AND password_hash = '' OR '1'='1' --';
- EXECUTED QUERY: SELECT * FROM users WHERE username = 'admin' AND password_hash = '' OR 
  1=1;--';

Evidence collected (files & location):
All evidence saved under: ./evidence/
- server_console.log — full server output (contains EXECUTED QUERY:).
- executed_queries_console.txt — extracted EXECUTED QUERY: lines (short).
- payloads.txt — the payload list used.
- sqli_success.png — screenshot of UI showing Login success after SQLi.
- devtools_network_sqli.png — DevTools screenshot showing POST /login with payload in Form 
  Data.
- sqli_attempt.har — HAR export of the login POST.
- db_dump_before_fix.txt — output of dump_db.py (users table snapshot).

Filenames are exact — please keep them when you add final artifacts so the report references stay valid.

Next steps for Member C (fixer)
- Replace the vulnerable query with parameterized queries (SQLite ? placeholders).
- Implement proper password hashing & verification (use bcrypt).
- Re-seed DB with hashed passwords if needed.
- Retest same payloads — they must not bypass auth.
- Collect AFTER-FIX evidence: executed_queries_console_afterfix.txt, new HAR/screenshot, and include a before/after comparison in the final report.
- Create PR / merge fixes into main once validated.

Contact: @HiralDinesh