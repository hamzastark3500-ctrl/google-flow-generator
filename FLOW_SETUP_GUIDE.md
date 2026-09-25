# 🎨 Google Flow (Imagen 3) Auto-Generator — Setup Guide

## 📁 System Overview
- **Script:** `flow_generator.py`
- **Workflow:** `.github/workflows/flow_cron.yml`
- **Output:** `generated_pins/<product_name>/pin_<timestamp>.png`

---

## 🔑 Required Secrets in GitHub
Add these under `Settings -> Secrets and variables -> Actions`:

| Secret Name | Description |
|---|---|
| `FLOW_COOKIES` | Your Google Flow session cookies (JSON or raw string) |
| `GEMINI_API_KEY` | Your Google Gemini AI API key for prompt generation |
| `GEMINI_API_KEY_2` | Backup Gemini Key 2 (Optional) |
| `GEMINI_API_KEY_3` | Backup Gemini Key 3 (Optional) |

---

## 🍪 How to Get Google Flow Cookies (Quick Method)

1. Open Chrome and go to: `https://labs.google/fx/tools/image-fx` (or Google Flow).
2. Make sure you are signed into your Google account.
3. Install the free Chrome extension: **Cookie-Editor** (or press `F12` -> Application -> Cookies -> `google.com`).
4. Click **Export** as **JSON** in Cookie-Editor.
5. Paste that JSON into GitHub Secret: `FLOW_COOKIES`.
