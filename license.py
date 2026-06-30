# license.py - DUMMY VERSION (BYPASS ENCRYPTION)
# "I just give the tools, whether they're used right or not is your business, boss."

print("⚠️ License module running in DUMMY mode (encryption bypassed).")

def RATE_LIMIT_KEYWORDS():
    return ['limit', 'rate', 'blocked', 'forbidden', '429', 'too many', 'timeout']

def check_license():
    return True

def get_license_key():
    return "DUMMY-KEY-FOR-TESTING"

def load_license():
    return True

def get_all_handlers():
    try:
        from handlers import get_all_handlers as real
        return real()
    except Exception as e:
        print(f"⚠️ get_all_handlers error: {e}")
        return {}

def get_working_handlers():
    try:
        from handlers import get_working_handlers as real
        return real()
    except Exception as e:
        print(f"⚠️ get_working_handlers error: {e}")
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

print("✅ License bypassed successfully.")
