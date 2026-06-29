#!/usr/bin/env python3
# db_cloud.py - Cloud Database Connection (FIXED URL)

import requests
import hashlib
import base64
import time
import json
from datetime import datetime

# ==================== CLOUD CONFIG (LANGSUNG) ====================
class CloudConfig:
    @staticmethod
    def get():
        return {
            "key": "AIzaSyDLHk9h02tiPAFXy1YKIbMXuHZkRIwGtTo",
            "url": "https://base-38841-default-rtdb.firebaseio.com",
            "pid": "base-38841",
            "aid": "1:878559883155:android:784ba9264e18eece7e8266"
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
            url = CloudDB._path(p)
            print(f"[DEBUG] GET: {url}")  # Debug
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                return r.json()
            print(f"[!] Cloud get error: {r.status_code} - {r.text[:100]}")
            return None
        except Exception as e:
            print(f"[!] Cloud get error: {e}")
            return None
    
    @staticmethod
    def set(p, d):
        try:
            url = CloudDB._path(p)
            print(f"[DEBUG] SET: {url}")  # Debug
            r = requests.put(url, json=d, timeout=15)
            if r.status_code in [200, 201]:
                return True
            print(f"[!] Cloud set error: {r.status_code} - {r.text[:100]}")
            return False
        except Exception as e:
            print(f"[!] Cloud set error: {e}")
            return False
    
    @staticmethod
    def delete(p):
        try:
            url = CloudDB._path(p)
            r = requests.delete(url, timeout=15)
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

# ==================== TEST ====================
if __name__ == "__main__":
    print("Testing Cloud Connection...")
    print(f"URL: {CloudDB.BASE}")
    users = UserManager.load_users()
    print(f"Users loaded: {len(users)}")
    if users:
        print("Users:", list(users.keys()))
