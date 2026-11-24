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

TOTAL_LOOPS = int(os.environ.get("LOOPS_PER_RUN", "40"))
MIN_DWELL = int(os.environ.get("MIN_DWELL", "12"))
MAX_DWELL = int(os.environ.get("MAX_DWELL", "20"))

GPU_PROFILES = [
    ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 7900 XTX Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)"),
]

SCREEN_PROFILES = [
    (1920, 1080),
    (1366, 768),
    (1536, 864),
    (1440, 900),
    (1600, 900),
    (2560, 1440),
    (1680, 1050),
    (1280, 720),
]

USER_AGENTS = [
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", "Win32"),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36", "Win32"),
    ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", "MacIntel"),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0", "Win32"),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0", "Win32"),
    ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", "Linux x86_64"),
]

def generate_stealth_js(canvas_seed: int, audio_seed: int, gpu_vendor: str,
                        gpu_renderer: str, screen_w: int, screen_h: int,
                        cores: int, memory: int, platform: str,
                        user_agent: str) -> str:
    """100% byte-for-byte fidelity replica of the original APK anti-detection hooks (a3.java)."""
    return f"""
    (function() {{
        try {{
            // 1. Clear automation & webdriver flags
            Object.defineProperty(navigator, 'webdriver', {{ get: () => undefined, configurable: true }});
            try {{ delete navigator.__proto__.webdriver; }} catch(e) {{}}

            const props = ['domAutomation', 'domAutomationController', '_selenium',
                           'callSelenium', '__webdriver_evaluate', '__driver_evaluate',
                           '__webdriver_unwrap', '__driver_unwrap', '__fxdriver_evaluate',
                           '__fxdriver_unwrap', '_Selenium_IDE_Recorder', 'calledSelenium',
                           '__nightmare', '_phantom', '__phantomas', 'domAutomation'];
            props.forEach(p => {{
                try {{ Object.defineProperty(window, p, {{ get: () => undefined, configurable: true }}); }} catch(e) {{}}
                try {{ Object.defineProperty(document, p, {{ get: () => undefined, configurable: true }}); }} catch(e) {{}}
            }});

            if (window.Notification) {{
                Object.defineProperty(Notification, 'permission', {{ get: () => 'default', configurable: true }});
            }}

            // 2. Mock authentic Chrome internals
            if (!window.chrome) {{
                window.chrome = {{
                    app: {{ isInstalled: false, InstallState: {{ DISABLED: 'disabled', INSTALLED: 'installed', NOT_INSTALLED: 'not_installed' }}, RunningState: {{ CANNOT_RUN: 'cannot_run', READY_TO_RUN: 'ready_to_run', RUNNING: 'running' }} }},
                    runtime: {{ PlatformOs: {{ MAC: 'mac', WIN: 'win', ANDROID: 'android', CROS: 'cros', LINUX: 'linux' }}, PlatformArch: {{ ARM: 'arm', X86_32: 'x86-32', X86_64: 'x86-64' }}, OnInstalledReason: {{ CHROME_UPDATE: 'chrome_update', INSTALL: 'install', SHARED_MODULE_UPDATE: 'shared_module_update', UPDATE: 'update' }} }}
                }};
            }}

            // 3. Hardware & Platform Overrides
            const overrides = {{
                platform: '{platform}',
                hardwareConcurrency: {cores},
                deviceMemory: {memory},
                maxTouchPoints: 0,
                language: 'en-US',
                languages: Object.freeze(['en-US', 'en']),
                vendor: 'Google Inc.',
                userAgent: '{user_agent}'
            }};
            for (const [key, value] of Object.entries(overrides)) {{
                try {{
                    Object.defineProperty(navigator, key, {{ get: () => value, configurable: true }});
                }} catch(e) {{}}
            }}

            // 4. Dynamic Screen Metrics
            Object.defineProperty(screen, 'width', {{ get: () => {screen_w}, configurable: true }});
            Object.defineProperty(screen, 'height', {{ get: () => {screen_h}, configurable: true }});
            Object.defineProperty(screen, 'availWidth', {{ get: () => {screen_w}, configurable: true }});
            Object.defineProperty(screen, 'availHeight', {{ get: () => {screen_h - 40}, configurable: true }});
            Object.defineProperty(screen, 'colorDepth', {{ get: () => 24, configurable: true }});
            Object.defineProperty(screen, 'pixelDepth', {{ get: () => 24, configurable: true }});
            Object.defineProperty(window, 'devicePixelRatio', {{ get: () => 1.0, configurable: true }});

            // 5. Canvas Noise Jitter (LCG PRNG from original a3.java)
            const SEED = {canvas_seed};
            let s = SEED;
            function nextRand() {{ s = (s * 16807 + 7) % 2147483647; return s; }}

            const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function() {{
                const imageData = origGetImageData.apply(this, arguments);
                const data = imageData.data;
                for (let i = 0; i < data.length; i += 4) {{
                    data[i] = (data[i] + (nextRand() % 3) - 1) & 0xFF;
                }}
                return imageData;
            }};

            const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function() {{
                const ctx = this.getContext('2d');
                if (ctx && this.width > 16 && this.height > 16) {{
                    try {{
                        const imgData = origGetImageData.call(ctx, 0, 0, Math.min(this.width, 100), Math.min(this.height, 100));
                        const d = imgData.data;
                        for (let i = 0; i < d.length; i += 4) {{
                            d[i] = (d[i] + (nextRand() % 3) - 1) & 0xFF;
                        }}
                        ctx.putImageData(imgData, 0, 0);
                    }} catch(e) {{}}
                }}
                return origToDataURL.apply(this, arguments);
            }};

            const origToBlob = HTMLCanvasElement.prototype.toBlob;
            HTMLCanvasElement.prototype.toBlob = function(callback) {{
                const ctx = this.getContext('2d');
                if (ctx && this.width > 16 && this.height > 16) {{
                    try {{
                        const imgData = origGetImageData.call(ctx, 0, 0, Math.min(this.width, 100), Math.min(this.height, 100));
                        const d = imgData.data;
                        for (let i = 0; i < d.length; i += 4) {{
                            d[i] = (d[i] + (nextRand() % 3) - 1) & 0xFF;
                        }}
                        ctx.putImageData(imgData, 0, 0);
                    }} catch(e) {{}}
                }}
                return origToBlob.apply(this, arguments);
            }};

            // 6. WebGL GPU Vendor & Renderer Spoofing
            const vendor = '{gpu_vendor}';
            const renderer = '{gpu_renderer}';
            const hook = (proto) => {{
                const getParam = proto.getParameter;
                proto.getParameter = function(param) {{
                    if (param === 37445) return vendor;
                    if (param === 37446) return renderer;
                    return getParam.apply(this, arguments);
                }};
            }};
            if (typeof WebGLRenderingContext !== 'undefined') hook(WebGLRenderingContext.prototype);
            if (typeof WebGL2RenderingContext !== 'undefined') hook(WebGL2RenderingContext.prototype);

            const origGetExtension = WebGLRenderingContext.prototype.getExtension;
            WebGLRenderingContext.prototype.getExtension = function(name) {{
                if (name === 'WEBGL_debug_renderer_info') return null;
                return origGetExtension.apply(this, arguments);
            }};

            // 7. AudioContext Noise Jitter
            let audioSeed = {audio_seed};
            function audioNoise() {{ audioSeed = (audioSeed * 16807 + 7) % 2147483647; return (audioSeed % 100) / 10000.0; }}

            if (typeof AnalyserNode !== 'undefined') {{
                const origGetFloatFreqData = AnalyserNode.prototype.getFloatFrequencyData;
                AnalyserNode.prototype.getFloatFrequencyData = function(array) {{
                    origGetFloatFreqData.apply(this, arguments);
                    for (let i = 0; i < array.length; i++) {{ array[i] += audioNoise(); }}
                }};
            }}
            if (typeof AudioBuffer !== 'undefined') {{
                const origGetChannelData = AudioBuffer.prototype.getChannelData;
                AudioBuffer.prototype.getChannelData = function() {{
                    const data = origGetChannelData.apply(this, arguments);
                    for (let i = 0; i < Math.min(data.length, 500); i++) {{ data[i] += audioNoise() * 0.0001; }}
                    return data;
                }};
            }}

            // 8. DOMRect / Element Bounding Jitter
            function jitterRect(r) {{
                const j = () => (nextRand() % 3 - 1) * 0.0001;
                return new DOMRect(r.x + j(), r.y + j(), r.width + j(), r.height + j());
            }}
            const origGetBCR = Element.prototype.getBoundingClientRect;
            Element.prototype.getBoundingClientRect = function() {{
                return jitterRect(origGetBCR.apply(this, arguments));
            }};

            // 9. WebRTC Block
            const noop = function(){{}};
            const blocked = function(){{ return {{
                createDataChannel: noop, createOffer: noop, createAnswer: noop,
                setLocalDescription: noop, setRemoteDescription: noop,
                close: noop, addEventListener: noop, removeEventListener: noop
            }};}};
            blocked.prototype = {{}};
            window.RTCPeerConnection = blocked;
            window.webkitRTCPeerConnection = blocked;
            window.mozRTCPeerConnection = blocked;
            if (navigator.mediaDevices) {{
                navigator.mediaDevices.getUserMedia = function() {{
                    return Promise.reject(new DOMException('Not allowed', 'NotAllowedError'));
                }};
                navigator.mediaDevices.enumerateDevices = function() {{ return Promise.resolve([]); }};
            }}
        }} catch(e) {{}}
    }})();
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

def run_single_loop(loop_idx: int) -> bool:
    ua_tuple = random.choice(USER_AGENTS)
    ua, platform = ua_tuple
    screen_w, screen_h = random.choice(SCREEN_PROFILES)
    canvas_seed = random.randint(1000000, 2147483647)
    audio_seed = random.randint(1000000, 2147483647)
    gpu_vendor, gpu_renderer = random.choice(GPU_PROFILES)
    cores = random.choice([4, 8, 12, 16])
    memory = random.choice([8, 16, 32])

    print(f"\n[LOOP #{loop_idx}/{TOTAL_LOOPS}] Spinning Up New Device Instance...")
    print(f" -> Resolution: {screen_w}x{screen_h} | Specs: {cores} Cores, {memory}GB RAM | OS: {platform}")
    print(f" -> GPU: {gpu_renderer[:36]}... | Seeds: Canvas({canvas_seed}), Audio({audio_seed})")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--lang=en-US,en")
    options.page_load_strategy = 'eager'

    options.add_argument(f"user-agent={ua}")
    options.add_argument(f"--window-size={screen_w},{screen_h}")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(35)
        driver.set_script_timeout(25)

        stealth_js = generate_stealth_js(
            canvas_seed=canvas_seed,
            audio_seed=audio_seed,
            gpu_vendor=gpu_vendor,
            gpu_renderer=gpu_renderer,
            screen_w=screen_w,
            screen_h=screen_h,
            cores=cores,
            memory=memory,
            platform=platform,
            user_agent=ua
        )

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": stealth_js
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

        print(f"[SUCCESS] Loop #{loop_idx} complete (Unique device session closed cleanly).")
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
    print("⚡ AUTOPILOT CLOUD 24/7 WORKER — DYNAMIC FINGERPRINT ENGINE")
    print(f"Target: {TARGET_URL if TARGET_URL else 'Dynamic Blog Rotation (6 URLs)'}")
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
