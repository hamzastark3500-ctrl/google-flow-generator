"""
=============================================================================
GOOGLE FLOW (IMAGEN 3) AUTO IMAGE GENERATOR & BULK DOWNLOADER
The Daily Reset Studio • AI Product Pin Graphics Engine
Playwright-Stealth • Multi-Account Cookie Engine • Human Rhythm
=============================================================================
"""

import os
import sys
import json
import time
import random
import argparse
from datetime import datetime
from pathlib import Path
from urllib import request

# UTF-8 encoding support
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


# 16 Products List for Pin Creation
PRODUCTS = [
    {"folder": "100_foods_before_one", "name": "100 Foods Before One | Baby BLW Feeding & Solids"},
    {"folder": "hormone_cycle_syncing", "name": "28-Day Hormone & Cycle Syncing Daily Wellness Planner"},
    {"folder": "kids_calm_down_corner", "name": "Kids Calm-Down Corner & Emotional Regulation Kit"},
    {"folder": "kids_health_hub", "name": "Kids Sickness, Medication & Pediatric Health Hub"},
    {"folder": "toddler_busy_binder", "name": "Toddler & Pre-K Learning Busy Binder Montessori Quiet Book"},
    {"folder": "boho_nursery_art", "name": "Boho Nursery Wall Art & Kids Room Decor Gallery Wall"},
    {"folder": "anxiety_shadow_work", "name": "Anxiety & Shadow Work Mental Reset Healing Journal"},
    {"folder": "screen_time_tokens", "name": "Kids Screen-Time Tokens & Chore Reward Bucks System"},
    {"folder": "date_night_cards", "name": "52-Week Creative Date Night Cards & Couples Romance Kit"},
    {"folder": "nanny_infant_log", "name": "Complete Nanny & Daycare Daily Infant Care Log Sheet"},
    {"folder": "sinking_funds_budget", "name": "Sinking Funds & Debt-Free Family Budget Binder"},
    {"folder": "dinner_meal_planner", "name": "4-Week Busy Mom Dinner & Grocery Budget System"},
    {"folder": "family_ice_binder", "name": "Family Emergency & ICE Important Documents Binder"},
    {"folder": "home_reset_cleaning", "name": "30-Day Home Reset & Deep Cleaning Routine System"},
    {"folder": "master_bundle_home_kids", "name": "Complete Home, Kitchen & Kids Reset Master Bundle"},
    {"folder": "master_bundle_wealth_emergency", "name": "Family Emergency, Wealth & Marriage Master Bundle"}
]


class GoogleFlowGenerator:
    def __init__(self, cookies_json=None, dry_run=False):
        self.dry_run = dry_run
        self.base_dir = Path(__file__).parent.resolve()
        self.output_dir = self.base_dir / "generated_pins"
        self.output_dir.mkdir(exist_ok=True)

        # Gemini Keys
        self.gemini_keys = []
        for k in ["GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3"]:
            val = (os.getenv(k) or "").strip()
            if val and val not in self.gemini_keys:
                self.gemini_keys.append(val)

        # Flow Cookies: Can be passed via env FLOW_COOKIES (JSON string or list)
        self.cookies_raw = cookies_json or os.getenv("FLOW_COOKIES") or ""
        self.cookies_list = self._parse_cookies(self.cookies_raw)

    def _parse_cookies(self, raw):
        """Parses cookies from JSON string, file, or semicolon string."""
        if not raw:
            c_file = self.base_dir / "cookies.json"
            if c_file.exists():
                try:
                    return json.loads(c_file.read_text(encoding="utf-8"))
                except Exception:
                    pass
            return []

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                for c in parsed:
                    c.setdefault("domain", ".google.com")
                    c.setdefault("path", "/")
                    if c.get("name", "").startswith("__Secure-") or c.get("name", "").startswith("__Host-"):
                        c["secure"] = True
                return parsed
            elif isinstance(parsed, dict):
                return [{"name": k, "value": v, "domain": ".google.com", "path": "/", "secure": True} for k, v in parsed.items()]
        except Exception:
            items = []
            for pair in raw.split(";"):
                if "=" in pair:
                    k, v = pair.strip().split("=", 1)
                    items.append({"name": k.strip(), "value": v.strip(), "domain": ".google.com", "path": "/", "secure": True})
            return items
        return []

    def generate_image_prompt(self, product_name):
        """Uses Gemini AI to generate a photorealistic Pinterest Pin design prompt."""
        if not self.gemini_keys:
            return (
                f"Aesthetic high-end Pinterest Pin mockup of {product_name}, modern clean pastel typography, "
                f"minimalist Scandinavian flat-lay desk with coffee, iPad, planner sheets, warm natural daylight, 8k resolution"
            )

        prompt_req = (
            f"Act as a professional graphic designer and Pinterest aesthetic curator.\n"
            f"Write an ULTRA-DETAILED text-to-image prompt for Google Imagen / Flow to create a viral Pinterest Pin graphic for:\n"
            f"Product: '{product_name}'\n\n"
            f"Rules:\n"
            f"1. Return ONLY the raw prompt text, no quotes, no explanations.\n"
            f"2. Style: Clean, aesthetic warm beige/cream tones, minimal Scandinavian flat-lay, warm morning sunlight, cozy desk aesthetic.\n"
            f"3. Must visually showcase a modern printable/digital planner page, iPad tablet mockup, and cute home decor stationery.\n"
            f"4. Under 350 characters, optimized for viral Pinterest CTR."
        )

        for key in self.gemini_keys:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                data = json.dumps({"contents": [{"parts": [{"text": prompt_req}]}]}).encode("utf-8")
                req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
                with request.urlopen(req, timeout=12) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                    print(f"   🤖 [Gemini AI Prompt]: {text[:60]}...")
                    return text
            except Exception:
                continue

        return f"Aesthetic minimalist Pinterest pin mockup for {product_name}, clean pastel flat-lay, 8k resolution, daylight"

    def run_browser_generator(self, product_folder, product_name, count=2):
        """Launches Playwright-Stealth Chromium to generate and download images from Google Flow / ImageFX."""
        if not PLAYWRIGHT_AVAILABLE:
            print("❌ Playwright is not installed!")
            return 0

        target_dir = self.output_dir / product_folder
        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n🎨 Starting generation for: {product_name}")
        print(f"📁 Target Folder: generated_pins/{product_folder}/")

        # Generate fresh prompt with Gemini
        ai_prompt = self.generate_image_prompt(product_name)

        if self.dry_run:
            print(f"   [DRY RUN] Would generate {count} images with prompt: {ai_prompt}")
            return count

        downloaded = 0
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )

            # Inject cookies if available
            if self.cookies_list:
                try:
                    context.add_cookies(self.cookies_list)
                    print(f"   🔑 Injected {len(self.cookies_list)} session cookies.")
                except Exception as ce:
                    print(f"   ⚠️ Cookie injection notice: {ce}")

            page = context.new_page()

            try:
                # Target Google Flow / ImageFX tool
                print("   🌐 Navigating to Google Labs ImageFX / Flow...")
                page.goto("https://labs.google/fx/tools/image-fx", wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(4000)

                # Check if login required
                if "accounts.google.com" in page.url.lower():
                    print("   ⚠️ Notice: Google redirected to login. Fresh cookies needed.")
                    page.screenshot(path=str(self.base_dir / "login_check.png"))
                    browser.close()
                    return 0

                # Type Prompt with human delay
                print("   ⌨️ Entering prompt into generation field...")
                prompt_input = page.locator('textarea, [contenteditable="true"], input[placeholder*="Describe" i]').first
                if prompt_input.count() > 0:
                    prompt_input.click()
                    # Human typing simulation
                    page.keyboard.type(ai_prompt, delay=random.randint(15, 35))
                    page.wait_for_timeout(1500)

                    # Click Generate button
                    gen_button = page.locator('button:has-text("Generate"), button:has-text("Create"), [aria-label*="Generate" i]').first
                    if gen_button.count() > 0:
                        gen_button.click()
                        print("   🚀 Clicked Generate! Waiting for AI to create images (30-45s)...")
                        
                        # Wait for image generation
                        page.wait_for_timeout(random.randint(30000, 45000))

                        # Find download buttons
                        download_buttons = page.locator('button[aria-label*="Download" i], button:has-text("Download")')
                        btn_count = download_buttons.count()
                        print(f"   📥 Found {btn_count} generated image(s). Downloading...")

                        for i in range(min(btn_count, count)):
                            try:
                                with page.expect_download(timeout=15000) as download_info:
                                    download_buttons.nth(i).click()
                                download = download_info.value
                                save_path = target_dir / f"pin_{int(time.time())}_{i+1}.png"
                                download.save_as(str(save_path))
                                print(f"   ✅ Saved: {save_path.name}")
                                downloaded += 1
                                page.wait_for_timeout(random.randint(2000, 4000))
                            except Exception as de:
                                print(f"   ⚠️ Download notice on item {i+1}: {de}")
                else:
                    print("   ⚠️ Prompt input field not found on current page layout.")
                    page.screenshot(path=str(self.base_dir / "page_debug.png"))

                browser.close()
                return downloaded

            except Exception as e:
                print(f"   ❌ Browser execution error: {e}")
                browser.close()
                return 0

    def start_batch(self, max_products=16, images_per_product=2):
        """Runs batch generation across products with human jitter intervals."""
        print("\n" + "="*70)
        print(f"🚀 GOOGLE FLOW AUTO-GENERATOR ENGINE STARTED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📦 Total Products to Process: {min(len(PRODUCTS), max_products)}")
        print(f"🎯 Target Images per Product: {images_per_product}")
        print("="*70 + "\n")

        total_downloaded = 0
        for idx, prod in enumerate(PRODUCTS[:max_products], 1):
            print(f"\n──────────────────────────────────────────────────────────────────────")
            print(f"[{idx}/{min(len(PRODUCTS), max_products)}] Processing: {prod['name']}")

            count = self.run_browser_generator(prod["folder"], prod["name"], count=images_per_product)
            total_downloaded += count

            # Natural Human Wait between products (20s to 45s)
            if idx < min(len(PRODUCTS), max_products):
                wait_sec = random.randint(20, 45)
                print(f"⏳ Human Rhythm Pause: Waiting {wait_sec}s before next product...")
                time.sleep(wait_sec)

        print("\n" + "="*70)
        print(f"🏁 BATCH COMPLETE: Total {total_downloaded} images generated & organized into folders!")
        print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Google Flow Auto Image Generator")
    parser.add_argument("--products", type=int, default=2, help="Number of products to process in this test run (default: 2)")
    parser.add_argument("--images-per-product", type=int, default=2, help="Images per product (default: 2)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without real browser session")
    args = parser.parse_args()

    generator = GoogleFlowGenerator(dry_run=args.dry_run)
    generator.start_batch(max_products=args.products, images_per_product=args.images_per_product)


if __name__ == "__main__":
    main()
