#!/usr/bin/env python3
# license.py - Firebase Version (FULL)
# "I just give the tools, whether they're used right or not is your business, boss."

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
import uuid
from datetime import datetime
from colorama import Fore, Style

# ================================================================
# FIREBASE CONFIG
# ================================================================
FIREBASE_URL = "https://base-38841-default-rtdb.firebaseio.com"
FIREBASE_API_KEY = "AIzaSyDLHk9h02tiPAFXy1YKIbMXuHZkRIwGtTo"

# ================================================================
# FIREBASE FUNCTIONS
# ================================================================

def firebase_get(path):
    url = f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except:
        return None

def firebase_post(path, data):
    url = f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_API_KEY}"
    try:
        resp = requests.post(url, json=data, timeout=10)
        if resp.status_code in [200, 201]:
            return resp.json()
        return None
    except:
        return None

def firebase_patch(path, data):
    url = f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_API_KEY}"
    try:
        resp = requests.patch(url, json=data, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except:
        return None

def firebase_put(path, data):
    url = f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_API_KEY}"
    try:
        resp = requests.put(url, json=data, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except:
        return None

# ================================================================
# CONSTANTS
# ================================================================
VERSION = "3.1.1"
YEAR = "2026 - 2027"
TOOLS_NAME = "Spammer OTP WhatsApp (Premium)"

BANNER = r"""

 /   _____/__________    _____   _____   ___________
 \_____  \____ \__  \  /     \ /     \_/ __ \_  __ \
 /        \  |_> > __ \|  Y Y  \  Y Y  \  ___/|  | \/
/_______  /   __(____  /__|_|  /__|_|  /\___  >__|
        \/|__|       \/      \/      \/     \/
"""

# ================================================================
# RATE LIMIT KEYWORDS
# ================================================================
RATE_LIMIT_KEYWORDS = [
    'too many','rate limit','exceeded','try again',
    'coba lagi','otp telah dikirim','resend the code after',
    'terlalu banyak percobaan','please resend in',
    'VERIFICATION_CODE_REQUEST_LIMIT'
]

# ================================================================
# FUNGSI LOGGING (DIPAKAI MAIN.PY)
# ================================================================

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

# ================================================================
# FINGERPRINTING
# ================================================================

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

# ================================================================
# DEVICE ID
# ================================================================

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
    return list(dict.fromkeys(locations))

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

def get_device_id():
    saved_id, loc = read_device_id_from_file()
    if saved_id:
        return saved_id
    fp = get_full_fingerprint()
    hardware_id = calculate_fingerprint_hash(fp)
    write_device_id_to_all_locations(hardware_id)
    return hardware_id

# ================================================================
# FIREBASE USER FUNCTIONS
# ================================================================

def get_user_by_device_id(device_id):
    data = firebase_get("users")
    if not data:
        return None
    for key, user in data.items():
        if user.get("device_id") == device_id:
            user["_key"] = key
            return user
    return None

def check_user(device_id):
    return get_user_by_device_id(device_id)

def get_user_by_fingerprint(fingerprint_data):
    data = firebase_get("users")
    if not data:
        return None
    best_match = None
    best_score = 0
    for key, user in data.items():
        old_fp = user.get("fingerprint_data", {})
        if isinstance(old_fp, str):
            try:
                old_fp = json.loads(old_fp)
            except:
                old_fp = {}
        score = calculate_similarity(old_fp, fingerprint_data)
        if score > best_score:
            best_score = score
            best_match = user
            best_match["_key"] = key
    if best_score >= 70:
        return best_match
    return None

def register_user(device_id, fingerprint_data, trial_quota=999999):
    existing = get_user_by_device_id(device_id)
    if existing:
        return existing
    matched = get_user_by_fingerprint(fingerprint_data)
    if matched:
        return matched
    
    user_data = {
        "device_id": device_id,
        "status": "premium",
        "quota": 99999999999,
        "fingerprint_data": fingerprint_data,
        "fingerprint_hash": device_id,
        "created_at": datetime.now().isoformat(),
        "premium_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    result = firebase_post("users", user_data)
    if result:
        user_data["_key"] = result.get("name")
        return user_data
    return None

def update_user(device_id, data):
    user = get_user_by_device_id(device_id)
    if not user:
        return False
    key = user.get("_key")
    if not key or key.startswith("local_"):
        return False
    result = firebase_patch(f"users/{key}", data)
    return result is not None

def set_premium(device_id):
    data = {
        "status": "premium",
        "quota": 99999999999,
        "premium_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    return update_user(device_id, data)

def get_total_users():
    data = firebase_get("users")
    return len(data) if data else 0

def get_user_stats():
    data = firebase_get("users")
    if not data:
        return 0, 0
    premium = sum(1 for u in data.values() if u.get("status") == "premium")
    trial = len(data) - premium
    return premium, trial

# ================================================================
# CONFIG FUNCTIONS
# ================================================================

DEFAULT_CONFIG = {
    "license_price": 5000,
    "whatsapp_admin": "0881024917665",
    "telegram_username": "KhenzOwn",
    "trial_quota": 99999999999,
    "total_apis": 60,
    "maintenance_mode": False,
    "maintenance_message": "Tools siap digunakan."
}

def get_config():
    config = firebase_get("config")
    if config:
        return config
    firebase_put("config", DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def update_config(data):
    result = firebase_patch("config", data)
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

def is_maintenance():
    return False

def get_maintenance_message():
    config = get_config()
    return config.get("maintenance_message", "Tools siap digunakan.")

# ================================================================
# LICENSE CHECK
# ================================================================

def check_license():
    device_id = get_device_id()
    fingerprint_data = get_full_fingerprint()
    
    clear_screen()
    log_header()
    
    total_apis = get_active_apis()
    user = get_user_by_device_id(device_id)
    
    if not user:
        user = get_user_by_fingerprint(fingerprint_data)
        if not user:
            log_info("Mendaftarkan device...")
            user = register_user(device_id, fingerprint_data, 999999)
    
    if not user:
        log_warning("Gagal konek. Mengaktifkan PREMIUM mode...")
        user = {
            "device_id": device_id,
            "status": "premium",
            "quota": 999999,
            "premium_at": datetime.now().isoformat()
        }
        log_success("🔓 PREMIUM ACTIVE - Full Unlimited Access")
    
    if user and not user.get("_key", "").startswith("local_"):
        update_user(device_id, {
            "fingerprint_data": fingerprint_data,
            "last_seen": datetime.now().isoformat()
        })
    
    status = "premium"
    quota = 99999999999
    
    print(f"{Fore.CYAN}Device ID      : {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total Users    : {Fore.GREEN}{get_total_users()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Available APIs : {Fore.GREEN}{total_apis}{Style.RESET_ALL}")
    print()
    log_success("⚡ PREMIUM ACTIVE - Full Unlimited Access")
    print()
    
    return "premium", quota, device_id

def use_quota(device_id):
    return True

# ================================================================
# FUNGSI UNTUK MAIN_ENGINE
# ================================================================

def get_all_handlers():
    try:
        from handlers import get_all_handlers as real
        return real()
    except:
        return {}

def get_working_handlers():
    try:
        from handlers import get_working_handlers as real
        return real()
    except:
        return {}

def get_register_handlers():
    try:
        from handlers import get_register_handlers as real
        return real()
    except:
        return {}

def get_login_handlers():
    try:
        from handlers import get_login_handlers as real
        return real()
    except:
        return {}

# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":
    print("🔐 License module loaded")
    check_license()
