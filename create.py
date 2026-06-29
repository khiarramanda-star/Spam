from db_cloud import UserManager
import platform

username = input("username: ")
password = input("password: ")
device_id = platform.node()

success, msg = UserManager.register(username, password, device_id, "ADMINGANTENGBGT")
print(msg)
