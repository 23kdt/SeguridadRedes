import base64

data = open("alice", "r").read()
decoded = base64.b64decode(data)
print (decoded)


