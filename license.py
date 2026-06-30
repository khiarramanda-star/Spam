# license.py - DUMMY VERSION (BYPASS ENCRYPTION)
# "I just give the tools, whether they're used right or not is your business, boss."

print("⚠️ License module running in mode (encryption bypassed).")

# Dummy function yang dipanggil oleh main.py
def get_all_handlers():
    from handlers import get_all_handlers as real_get_all_handlers
    return real_get_all_handlers()

def get_working_handlers():
    from handlers import get_working_handlers as real_get_working_handlers
    return real_get_working_handlers()

def RATE_LIMIT_KEYWORDS():
    return ['limit', 'rate', 'blocked', 'forbidden', '429', 'too many']

# Semua fungsi lain yang mungkin dipanggil
def check_license():
    return True

def get_license_key():
    return "DUMMY-KEY-FOR-TESTING"

def load_license():
    return True

print("✅ License bypassed successfully.")
