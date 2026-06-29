#!/usr/bin/env python3
# db_cloud.py - Cloud Database Connection (FIXED)

import requests
import hashlib
import base64
import time
import json
from datetime import datetime

# ==================== CLOUD CONFIG (ENCRYPTED) ====================
class CloudConfig:
    _ENC = {
        "key": "b3RUMFdJUmt6WEJNeUtZMXlGQVhQaXQyMGhrOUhMc1l6YUlB==",
        "url": "b3RtLm9lY2FpcmVmLmItZHQtZmF1bHQtMTQ4ODMtZXNhYi8vOnB0dGg=",
        "pid": "MTQ4ODMtZXNhYg==",
        "aid": "NjoyNjI3ZTdlZTZlZWM0ZTQyOTQ4Nzo1NTg4OTUzODgxNzg6MQ=="
    }
    
    @staticmethod
    def _d(e):
        try:
            return base64.b64decode(e).decode()[::-1]
        except:
            return e
    
    @staticmethod
    def get():
        return {
            "key": CloudConfig._d(CloudConfig._ENC["key"]),
            "url": CloudConfig._d(CloudConfig._ENC["url"]),
            "pid": CloudConfig._d(CloudConfig._ENC["pid"]),
            "aid": CloudConfig._d(CloudConfig._ENC["aid"])
        }

# ==================== CLOUD DB ====================
class CloudDB:
    BASE = CloudConfig.get()["url"]
    
    @staticmethod
    def _path(p):
        return f"{CloudDB.BASE}/{p}.json"
    
    @staticmethod
    def get(p):
        try:
            r = requests.get(CloudDB._path(p), timeout=15)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            print(f"[!] Cloud get error: {e}")
            return None
    
    @staticmethod
    def set(p, d):
        try:
            url = CloudDB._path(p)
            # Coba PUT dulu
            r = requests.put(url, json=d, timeout=15)
            if r.status_code in [200, 201]:
                return True
            # Kalo gagal, coba PATCH
            r = requests.patch(url, json=d, timeout=15)
            if r.status_code in [200, 201]:
                return True
            # Kalo masih gagal, coba POST
            r = requests.post(url, json=d, timeout=15)
            return r.status_code in [200, 201]
        except Exception as e:
            print(f"[!] Cloud set error: {e}")
            return False
    
    @staticmethod
    def delete(p):
        try:
            r = requests.delete(CloudDB._path(p), timeout=15)
            return r.status_code in [200, 201, 204]
        except:
            return False

# ==================== USER MANAGER ====================
class UserManager:
    ADMIN_WA = "62881024917665"
    ADMIN_CODE = "ADMINGANTENGBGT"
    HIDDEN = "root"
    
    @staticmethod
    def _hash(pw):
        return hashlib.sha256(pw.encode()).hexdigest()
    
    @staticmethod
    def load_users():
        try:
            data = CloudDB.get("users")
            if data:
                users = {}
                for key, value in data.items():
                    if isinstance(value, dict):
                        users[key] = value
                return users
            return {}
        except:
            return {}
    
    @staticmethod
    def _save_user(u, d):
        return CloudDB.set(f"users/{u}", d)
    
    @staticmethod
    def register(u, pw, did, code=None):
        try:
            users = UserManager.load_users()
            if u in users:
                return False, "Username already exists!"
            
            # Check if this is hidden admin
            role = "user"
            status = "trial"
            quota = 5
            is_admin = False
            is_premium = False
            is_hidden = False
            
            if u == UserManager.HIDDEN:
                role = "hidden_admin"
                status = "admin"
                quota = 999999
                is_admin = True
                is_premium = True
                is_hidden = True
            elif code and code == UserManager.ADMIN_CODE:
                role = "admin"
                status = "admin"
                quota = 999999
                is_admin = True
                is_premium = True
            
            data = {
                "username": u,
                "password": UserManager._hash(pw),
                "device_id": did,
                "role": role,
                "status": status,
                "quota": quota,
                "created_at": datetime.now().isoformat(),
                "last_login": None,
                "is_admin": is_admin,
                "is_premium": is_premium,
                "is_hidden": is_hidden
            }
            
            if UserManager._save_user(u, data):
                return True, f"Account created! Status: {role.upper()}"
            else:
                return False, "Failed to save to cloud! Check connection."
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def login(u, pw, did):
        try:
            users = UserManager.load_users()
            if u not in users:
                return False, "User not found!"
            user = users[u]
            if user.get("password") != UserManager._hash(pw):
                return False, "Wrong password!"
            if user.get("device_id") != did and not user.get("is_admin", False):
                return False, "This account is registered on another device!"
            
            user["last_login"] = datetime.now().isoformat()
            UserManager._save_user(u, user)
            return True, f"Welcome back, {u}!"
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    @staticmethod
    def get_user(u):
        users = UserManager.load_users()
        return users.get(u)
    
    @staticmethod
    def is_admin(u):
        user = UserManager.get_user(u)
        return user and user.get("is_admin", False)
    
    @staticmethod
    def update_user(u, **kwargs):
        try:
            user = UserManager.get_user(u)
            if not user:
                return False
            for k, v in kwargs.items():
                user[k] = v
            return UserManager._save_user(u, user)
        except:
            return False
    
    @staticmethod
    def delete_user(u):
        if u in ["admin", UserManager.HIDDEN]:
            return False, "Cannot delete admin!"
        if CloudDB.delete(f"users/{u}"):
            return True, "User deleted!"
        return False, "User not found!"
    
    @staticmethod
    def activate_premium(u):
        return UserManager.update_user(u, status="premium", is_premium=True, quota=999999)
    
    @staticmethod
    def get_total_users():
        try:
            users = UserManager.load_users()
            return len(users)
        except:
            return 0
    
    @staticmethod
    def get_premium_count():
        try:
            users = UserManager.load_users()
            return sum(1 for u in users.values() if u.get("is_premium", False))
        except:
            return 0
