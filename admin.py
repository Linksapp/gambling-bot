from config import admins
from sys import maxsize

def check_privilege(chat_id):
    if chat_id in admins:
        return maxsize
    else:
        return 1000