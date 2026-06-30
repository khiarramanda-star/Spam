import os
import sys
import hashlib
import platform
import requests
import subprocess
import re
import json
import time
import random
import string
from datetime import datetime
from colorama import Fore, Style

# ==================== TABLES ====================
TABLE_USERS = "users"
TABLE_CONFIG = "config"
TABLE_FINGERPRINTS = "fingerprints"
TABLE_USAGE_LOGS = "usage_logs"

# ==================== DEFAULT CONFIG ====================
DEFAULT_CONFIG = {
    "license_price": 5000,
    "whatsapp_admin": "0881024917665",
    "telegram_username": "KhenzOwn",
    "trial_quota": 99999999999,
    "total_apis": 60,
    "maintenance_mode": False,
    "maintenance_message": "Tools sedang dalam pemeliharaan. Mohon tunggu hingga selesai."
}

# ==================== VERSION ====================
VERSION = "1"
YEAR = "2026 - 2027"
TOOLS_NAME = "Spammer OTP WhatsApp (Premium)"

# ==================== BANNER ====================
BANNER = r"""

 /   _____/__________    _____   _____   ___________
 \_____  \____ \__  \  /     \ /     \_/ __ \_  __ \
 /        \  |_> > __ \|  Y Y  \  Y Y  \  ___/|  | \/
/_______  /   __(____  /__|_|  /__|_|  /\___  >__|
        \/|__|       \/      \/      \/     \/
"""

# ==================== RATE LIMIT KEYWORDS ====================
RATE_LIMIT_KEYWORDS = [
    'too many','rate limit','exceeded','try again',
    'coba lagi','otp telah dikirim','resend the code after',
    'terlalu banyak percobaan','please resend in',
    'VERIFICATION_CODE_REQUEST_LIMIT'
]

# ==================== FUNGSI ====================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_info(msg):
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {msg}")

def log_success(msg):
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")

def log_warning(msg):
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {msg}")

def log_error(msg):
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")

def log_input(prompt):
    return input(f"{Fore.YELLOW}?{Style.RESET_ALL} {prompt}")

def log_header():
    clear_screen()
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Spammer OTP WhatsApp v.{VERSION} {Fore.WHITE}©{YEAR}{Style.RESET_ALL}")
    print()

def log_admin_header():
    clear_screen()
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}ADMIN PANEL - Spammer OTP WhatsApp v.{VERSION} {Fore.WHITE}©{YEAR}{Style.RESET_ALL}")
    print()

# ==================== FINGERPRINTING ====================

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return '127.0.0.1'

def get_machine_id():
    try:
        if platform.system() == "Windows":
            cmd = "wmic csproduct get uuid /value"
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            match = re.search(r'UUID=(.+)', output)
            if match:
                return match.group(1).strip()
        else:
            paths = ["/etc/machine-id", "/var/lib/dbus/machine-id"]
            for path in paths:
                try:
                    with open(path, "r") as f:
                        uid = f.read().strip()
                        if uid:
                            return uid
                except:
                    pass
    except:
        pass
    return None

def get_android_id():
    try:
        if os.path.exists("/data/system/users/0/settings_secure.xml"):
            with open("/data/system/users/0/settings_secure.xml", "r") as f:
                content = f.read()
                match = re.search(r'android_id"\s+value="([^"]+)"', content)
                if match:
                    return match.group(1)
    except:
        pass
    return None

def get_product_uuid():
    try:
        if platform.system() == "Linux":
            paths = [
                "/sys/class/dmi/id/product_uuid",
                "/sys/devices/virtual/dmi/id/product_uuid"
            ]
            for path in paths:
                try:
                    with open(path, "r") as f:
                        uuid_val = f.read().strip()
                        if uuid_val:
                            return uuid_val
                except:
                    pass
    except:
        pass
    return None

def get_cpu_info():
    try:
        if platform.system() == "Linux":
            with open("/proc/cpuinfo", "r") as f:
                content = f.read()
                match = re.search(r'model name\s*:\s*(.+)', content)
                cpu = match.group(1).strip()[:30] if match else "unknown"
                match = re.search(r'processor\s*:\s*(\d+)', content)
                cores = int(match.group(1)) + 1 if match else 1
                return f"{cpu}_{cores}cores"
    except:
        pass
    return None

def get_device_model():
    try:
        if os.path.exists("/system/bin/getprop"):
            cmd = "getprop ro.product.model"
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            if output:
                return output
    except:
        pass
    return None

def get_build_fingerprint():
    try:
        if os.path.exists("/system/bin/getprop"):
            cmd = "getprop ro.build.fingerprint"
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            if output:
                return output
    except:
        pass
    return None

def get_mac_address():
    try:
        import uuid
        mac = uuid.getnode()
        if mac:
            return f"{mac:012x}"
    except:
        pass
    return None

def get_full_fingerprint():
    return {
        "machine_id": get_machine_id(),
        "android_id": get_android_id(),
        "product_uuid": get_product_uuid(),
        "cpu_info": get_cpu_info(),
        "device_model": get_device_model(),
        "build_fingerprint": get_build_fingerprint(),
        "mac_address": get_mac_address(),
        "hostname": platform.node(),
        "platform": platform.system(),
        "platform_release": platform.release()
    }

def calculate_fingerprint_hash(fingerprint_data):
    clean_data = {k: v for k, v in fingerprint_data.items() if v}
    if not clean_data:
        clean_data = {"fallback": f"{platform.node()}_{os.path.abspath('/')}"}
    raw = "|".join([f"{k}:{v}" for k, v in sorted(clean_data.items())])
    return hashlib.sha256(raw.encode()).hexdigest()[:32]

def calculate_similarity(old_data, new_data):
    weights = {
        "machine_id": 30,
        "android_id": 30,
        "product_uuid": 20,
        "cpu_info": 10,
        "device_model": 5,
        "mac_address": 3,
        "hostname": 2
    }

    score = 0
    total_weight = sum(weights.values())

    for key, weight in weights.items():
        old_val = old_data.get(key)
        new_val = new_data.get(key)

        if old_val and new_val and old_val == new_val:
            score += weight

    return int((score / total_weight) * 100) if total_weight > 0 else 0

# ==================== DEVICE ID ====================

def get_device_id_locations():
    termux_share = "/data/data/com.termux/files/usr/share/.device.id"

    locations = [termux_share]
    locations.append(".device.id")
    locations.append(os.path.expanduser("~/.device.id"))

    if platform.system() != "Windows":
        locations.extend([
            "/sdcard/Download/.device.id",
            "/sdcard/Pictures/.device.id",
            "/sdcard/DCIM/.device.id",
            "/sdcard/Movies/.device.id",
            "/data/local/tmp/.device.id",
        ])

    locations.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".device.id"))

    seen = set()
    unique = []
    for loc in locations:
        if loc not in seen:
            seen.add(loc)
            unique.append(loc)
    return unique

def read_device_id_from_file():
    for loc in get_device_id_locations():
        try:
            if os.path.exists(loc):
                with open(loc, "r") as f:
                    saved_id = f.read().strip()
                    if len(saved_id) == 32:
                        return saved_id, loc
        except:
            pass
    return None, None

def write_device_id_to_all_locations(device_id):
    success_count = 0
    for loc in get_device_id_locations():
        try:
            os.makedirs(os.path.dirname(loc), exist_ok=True)
            with open(loc, "w") as f:
                f.write(device_id)
            success_count += 1
        except:
            pass
    return success_count >= 1

def verify_device_id_files(device_id):
    existing = []
    missing = []
    for loc in get_device_id_locations():
        try:
            if os.path.exists(loc):
                with open(loc, "r") as f:
                    saved = f.read().strip()
                    if saved == device_id:
                        existing.append(loc)
                    else:
                        missing.append(loc)
            else:
                missing.append(loc)
        except:
            missing.append(loc)
    return existing, missing

def get_device_id():
    saved_id, loc = read_device_id_from_file()
    if saved_id:
        existing, missing = verify_device_id_files(saved_id)
        if missing:
            for m in missing:
                try:
                    os.makedirs(os.path.dirname(m), exist_ok=True)
                    with open(m, "w") as f:
                        f.write(saved_id)
                except:
                    pass
        return saved_id

    fp = get_full_fingerprint()
    hardware_id = calculate_fingerprint_hash(fp)

# ==================== CONFIG ====================
def get_config():
    result = supabase_request("GET", f"{TABLE_CONFIG}?id=eq.1")
    if result and len(result) > 0:
        return result[0]
    else:
        default = {
            "id": 1,
            "license_price": DEFAULT_CONFIG["license_price"],
            "whatsapp_admin": DEFAULT_CONFIG["whatsapp_admin"],
            "telegram_username": DEFAULT_CONFIG["telegram_username"],
            "trial_quota": DEFAULT_CONFIG["trial_quota"],
            "total_apis": DEFAULT_CONFIG["total_apis"],
            "maintenance_mode": DEFAULT_CONFIG["maintenance_mode"],
            "maintenance_message": DEFAULT_CONFIG["maintenance_message"]
        }
        supabase_request("POST", TABLE_CONFIG, default)
        return default

def update_config(data):
    result = supabase_request("PATCH", f"{TABLE_CONFIG}?id=eq.1", data)
    return result is not None

def get_license_price():
    config = get_config()
    return config.get("license_price", DEFAULT_CONFIG["license_price"])

def get_whatsapp_admin():
    config = get_config()
    return config.get("whatsapp_admin", DEFAULT_CONFIG["whatsapp_admin"])

def get_telegram_username():
    config = get_config()
    return config.get("telegram_username", DEFAULT_CONFIG["telegram_username"])

def get_trial_quota():
    config = get_config()
    return config.get("trial_quota", DEFAULT_CONFIG["trial_quota"])

def get_active_apis():
    config = get_config()
    return config.get("total_apis", DEFAULT_CONFIG["total_apis"])

# ==========================================
# MODIFIKASI: MAINTENANCE MODE DIPAKSA MATI
# ==========================================
def is_maintenance():
    return False  # Paksa mati, tidak peduli database

def get_maintenance_message():
    return "Tools siap digunakan."

# ==================== USERS ====================
def get_user_by_device_id(device_id):
    result = supabase_request("GET", f"{TABLE_USERS}?device_id=eq.{device_id}")
    if result and len(result) > 0:
        return result[0]
    return None

def check_user(device_id):
    return get_user_by_device_id(device_id)

def get_user_by_fingerprint(fingerprint_data):
    all_fingerprints = supabase_request("GET", TABLE_FINGERPRINTS)
    if not all_fingerprints:
        return None

    best_match = None
    best_score = 0

    for fp_record in all_fingerprints:
        old_data = fp_record.get("fingerprint_data", {})
        if isinstance(old_data, str):
            try:
                old_data = json.loads(old_data)
            except:
                old_data = {}

        score = calculate_similarity(old_data, fingerprint_data)

        if score > best_score:
            best_score = score
            best_match = fp_record

    if best_score >= 70:
        user_id = best_match.get("user_id")
        if user_id:
            user = supabase_request("GET", f"{TABLE_USERS}?id=eq.{user_id}")
            if user and len(user) > 0:
                return user[0]

    return None

def register_user(device_id, fingerprint_data, trial_quota=999999):
    existing = get_user_by_device_id(device_id)
    if existing:
        return existing

    matched = get_user_by_fingerprint(fingerprint_data)
    if matched:
        return matched

    ip = get_public_ip()

    # ==========================================
    # MODIFIKASI: REGISTRASI LANGSUNG PREMIUM
    # ==========================================
    user_data = {
        "device_id": device_id,
        "status": "premium",
        "quota": 99999999999,
        "premium_at": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    result = supabase_request("POST", TABLE_USERS, user_data)

    # ==========================================
    # PERBAIKAN: TIDAK LANGSUNG EXIT
    # ==========================================
    if not result or len(result) == 0:
        log_error("Gagal mendaftarkan. Sedang Mengaktifkan PREMIUM mode...")

        # Buat user lokal (tanpa database) agar tetap bisa jalan
        user = {
            "id": "local_" + device_id[:8],
            "device_id": device_id,
            "status": "premium",
            "quota": 99999999999,
            "premium_at": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        log_success("🔓 PREMIUM ACTIVE ")
        return user

    user = result[0]
    user_id = user.get("id")

    fp_data = {
        "user_id": user_id,
        "fingerprint_data": json.dumps(fingerprint_data),
        "fingerprint_hash": device_id,
        "score": 100,
        "created_at": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat()
    }
    supabase_request("POST", TABLE_FINGERPRINTS, fp_data)

    log_data = {
        "user_id": user_id,
        "action": "register_premium",
        "ip": ip,
        "user_agent": "python-requests",
        "timestamp": datetime.now().isoformat()
    }
    supabase_request("POST", TABLE_USAGE_LOGS, log_data)

    return user

def update_user(device_id, data):
    result = supabase_request("PATCH", f"{TABLE_USERS}?device_id=eq.{device_id}", data)
    return result is not None

def update_fingerprint(device_id, fingerprint_data):
    user = get_user_by_device_id(device_id)
    if not user:
        return False

    user_id = user.get("id")

    existing = supabase_request("GET", f"{TABLE_FINGERPRINTS}?user_id=eq.{user_id}")
    if existing and len(existing) > 0:
        supabase_request("PATCH",
            f"{TABLE_FINGERPRINTS}?user_id=eq.{user_id}",
            {"last_seen": datetime.now().isoformat()}
        )
    else:
        fp_data = {
            "user_id": user_id,
            "fingerprint_data": json.dumps(fingerprint_data),
            "fingerprint_hash": device_id,
            "score": 100,
            "last_seen": datetime.now().isoformat()
        }
        supabase_request("POST", TABLE_FINGERPRINTS, fp_data)

    return True

def set_premium(device_id):
    data = {
        "status": "premium",
        "quota": 99999999999,
        "premium_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    return update_user(device_id, data)

def get_total_users():
    result = supabase_request("GET", TABLE_USERS)
    if result:
        return len(result)
    return 0

def get_user_stats():
    result = supabase_request("GET", TABLE_USERS)
    if not result:
        return 0, 0

    premium = sum(1 for u in result if u.get("status") == "premium")
    trial = len(result) - premium
    return premium, trial

# ==================== ADMIN NUMBER CHECK ====================
ADMIN_NUMBERS = ["0881024917665", "62881024917665", "+62881024917665"]

def is_admin_number(phone):
    phone = phone.strip().replace(' ', '').replace('-', '').replace('+', '')
    return phone in ADMIN_NUMBERS or phone.endswith("881024917665")

# ==================== LICENSE CHECK (FULL PREMIUM + OFFLINE) ====================
def check_license():
    device_id = get_device_id()
    fingerprint_data = get_full_fingerprint()

    clear_screen()
    log_header()

    # ==========================================
    # BYPASS MAINTENANCE - LANGSUNG PREMIUM
    # ==========================================
    total_apis = get_active_apis()

    user = get_user_by_device_id(device_id)

    if not user:
        user = get_user_by_fingerprint(fingerprint_data)

        if not user:
            log_info("Mendaftarkan device...")
            user = register_user(device_id, fingerprint_data, 999999)

            # ==========================================
            # PERBAIKAN: CEK APAKAH USER VALID
            # ==========================================
            if not user:
                log_warning("Gagal konek. Mengaktifkan PREMIUM mode...")
                # Buat user lokal dummy
                user = {
                    "device_id": device_id,
                    "status": "premium",
                    "quota": 999999,
                    "premium_at": datetime.now().isoformat()
                }
                log_success("🔓 PREMIUM ACTIVE - Full Unlimited Access ")
            else:
                log_success("Pendaftaran berhasil! (Premium Active)")
        else:
            log_info("Perangkat dikenali (fingerprint match). Memuat data...")
            update_user(user["device_id"], {
                "device_id": device_id,
                "status": "premium",
                "quota": 99999999999
            })
            user = get_user_by_device_id(device_id)
    else:
        # ==========================================
        # PASTIKAN SEMUA USER PREMIUM
        # ==========================================
        if user.get("status") != "premium":
            update_user(device_id, {
                "status": "premium",
                "quota": 99999999999,
                "premium_at": datetime.now().isoformat()
            })
            user = get_user_by_device_id(device_id)

        update_fingerprint(device_id, fingerprint_data)

    # ==========================================
    # PASTIKAN STATUS PREMIUM
    # ==========================================
    status = "premium"
    quota = 99999999999

    print(f"{Fore.CYAN}Device ID      : {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total Users    : {Fore.GREEN}{get_total_users()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Available APIs : {Fore.GREEN}{total_apis}{Style.RESET_ALL}")
    print()

    log_success("⚡ PREMIUM ACTIVE - Full Unlimited Access")
    print()

    return "premium", quota, device_id

# ==========================================
# USE_QUOTA TIDAK MENGURANGI APAPUN
# ==========================================
def use_quota(device_id):
    return True
============================================================
