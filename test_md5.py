import hashlib
if __name__ == "__main__":
    B = hashlib.sha224("passwpord").hexdigest()
    print B