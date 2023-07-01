from base64 import b64encode, b64decode

data = "1233232/456323/Modern Realm"
print(b64encode(data.encode()).decode())
