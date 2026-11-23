import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TARGET_URLS = [
    "https://zerotoherostoriess.blogspot.com/2026/11/from-five-hour-bus-rides-to-egyptian.html",
    "https://zerotoherostoriess.blogspot.com/2026/11/he-lost-70-billion-then-came-back.html",
    "https://zerotoherostoriess.blogspot.com/2026/11/from-two-room-flat-in-chennai-to-top-of.html",
    "https://zerotoherostoriess.blogspot.com/2026/11/from-bomb-shelters-to-24-grand-slams.html",
    "https://zerotoherostoriess.blogspot.com/2026/11/he-washed-dishes-for-120-hour-then.html",
    "https://zerotoherostoriess.blogspot.com/2026/11/sent-to-orphanage-at-seven-then-he.html",
]

TARGET_URL = os.environ.get("TARGET_URL", "")

TOTAL_LOOPS = int(os.environ.get("LOOPS_PER_RUN", "25"))
MIN_DWELL = int(os.environ.get("MIN_DWELL", "15"))
MAX_DWELL = int(os.environ.get("MAX_DWELL", "30"))

STEALTH_JS = """
(function() {
    try {
        delete navigator.__proto__.webdriver;
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    } catch(e) {}

    window.chrome = {
        app: { isInstalled: false },
        runtime: {
            OnInstalledReason: { INSTALL: "install", UPDATE: "update", CHROME_UPDATE: "chrome_update" },
            OnRestartRequiredReason: { APP_UPDATE: "app_update", OS_UPDATE: "os_update", PERIODIC: "periodic" },
            PlatformArch: { X86_64: "x86-64" },
            PlatformOs: { LINUX: "linux", WIN: "win" }
        }
    };

    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 16 });

    // WebRTC Block
    window.RTCPeerConnection = function() { throw new Error('WebRTC disabled by policy'); };
    window.webkitRTCPeerConnection = function() { throw new Error('WebRTC disabled by policy'); };

    // WebGL Vendor Spoofing
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Google Inc. (NVIDIA)';
        if (parameter === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX Direct3D11 vs_5_0 ps_5_0, D3D11)';
        return getParameter.apply(this, arguments);
    };
})();
"""

SMOOTH_SCROLL_JS = """
(function(distance, duration) {
    const start = window.scrollY;
    let startTime = null;

    function easeInOutCubic(t) {
        return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3) / 2;
    }

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = easeInOutCubic(progress);
        window.scrollTo(0, start + distance * eased);
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
})(arguments[0], arguments[1]);
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

def run_single_loop(loop_idx: int) -> bool:
    print(f"\n[LOOP #{loop_idx}/{TOTAL_LOOPS}] Starting Cloud Session...")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--lang=en-US,en")
    options.page_load_strategy = 'eager'

    ua = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={ua}")
    w = random.randint(1280, 1920)
    h = random.randint(720, 1080)
    options.add_argument(f"--window-size={w},{h}")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(35)
        driver.set_script_timeout(25)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": STEALTH_JS
        })

        chosen_url = TARGET_URL if TARGET_URL else random.choice(TARGET_URLS)
        print(f"[NAVIGATING] {chosen_url}")
        driver.get(chosen_url)
        time.sleep(2.0)
        print(f"[LOADED] Title: {driver.title[:45] if driver.title else 'Active'}")

        # Deep Scroll Human Traversal
        dwell_time = random.randint(MIN_DWELL, MAX_DWELL)
        end_time = time.time() + dwell_time
        print(f"[HUMAN_SCROLL] Traversing with easeInOutCubic (Dwell: {dwell_time}s)...")

        while time.time() < end_time:
            # Random natural reader pause & focus
            if random.random() < 0.25:
                try:
                    driver.execute_script("""
                        const paras = document.querySelectorAll('.post-body p, article p, p');
                        if (paras.length > 0) {
                            const target = paras[Math.floor(Math.random() * paras.length)];
                            target.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                        }
                    """)
                except Exception:
                    pass

            curr_y = driver.execute_script("return window.scrollY;")
            page_h = driver.execute_script("return document.body.scrollHeight;")
            win_h = driver.execute_script("return window.innerHeight;")

            if curr_y + win_h >= page_h - 150:
                up_dist = -random.randint(300, 600)
                driver.execute_script(SMOOTH_SCROLL_JS, up_dist, 1200)
                time.sleep(2.0)
                continue

            if random.random() < 0.15 and curr_y > 400:
                back_dist = -random.randint(150, 300)
                driver.execute_script(SMOOTH_SCROLL_JS, back_dist, 800)
                time.sleep(1.2)
                continue

            dist = random.randint(250, 500)
            dur = random.randint(700, 1300)
            driver.execute_script(SMOOTH_SCROLL_JS, dist, dur)
            time.sleep(dur / 1000.0)

            pause = random.uniform(1.8, 3.8)
            time.sleep(pause)

        print(f"[SUCCESS] Loop #{loop_idx} complete (Organic dwell finished).")
        return True

    except Exception as e:
        print(f"[ERROR] Loop #{loop_idx} encountered: {e}")
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

def main():
    print("=" * 60)
    print("⚡ AUTOPILOT CLOUD 24/7 WORKER")
    print(f"Target: {TARGET_URL}")
    print(f"Planned Loops: {TOTAL_LOOPS}")
    print(f"Dwell Range: {MIN_DWELL}s - {MAX_DWELL}s")
    print("=" * 60)

    success_count = 0
    for i in range(1, TOTAL_LOOPS + 1):
        if run_single_loop(i):
            success_count += 1
        cooldown = random.uniform(2.0, 5.0)
        time.sleep(cooldown)

    print("\n" + "=" * 60)
    print(f"BATCH FINISHED: {success_count}/{TOTAL_LOOPS} Successful Visits Sent.")
    print("=" * 60)

if __name__ == "__main__":
    main()
