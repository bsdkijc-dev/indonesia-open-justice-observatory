# Source Access Policy — Indonesia Open Justice Observatory (IOJO)

## 1. Lawful & Conservative Access
IOJO collects only publicly accessible official judicial information. Public accessibility does **not** imply unrestricted permission to redistribute full source documents.

## 2. Pre-Collection Checklist
Before collecting from any source, the Source Agent must document:
1. Source owner and official URL.
2. Terms of use, copyright notice, and access restrictions.
3. `robots.txt` directives (if accessible).
4. Authorized access method (official PDF/CSV download, authorized API, or polite HTML metadata read).
5. Publication date, retrieval timestamp, coverage, and missing periods.

## 3. Technical Safeguards
- Conservative request rate (minimum 2.0–5.0 seconds delay between requests).
- Local response caching and duplicate-request prevention.
- Exponential backoff on HTTP 429/5xx responses.
- Immediate halt on CAPTCHA, authentication walls, or instability.
- **Never** bypass CAPTCHA, login gates, or rate limits.
