import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. CREATE client
client = {"name": "JYO", "email": "ksj@gmail.com"}
res = requests.post(f"{BASE_URL}/clients/", json=client)
print("CREATE:", res.json())

# Get client ID from response
client_id = res.json().get("id")

# 2. READ all clients
res = requests.get(f"{BASE_URL}/clients/")
print("READ ALL:", res.json())

# 3. UPDATE client
updated_client = {"name": "JYO Updated", "email": "ksjupdated@gmail.com"}
res = requests.put(f"{BASE_URL}/clients/{client_id}", json=updated_client)
print("UPDATE:", res.json())

# 4. READ single client
res = requests.get(f"{BASE_URL}/clients/{client_id}")
print("READ SINGLE:", res.json())

# 5. DELETE client
res = requests.delete(f"{BASE_URL}/clients/{client_id}")
print("DELETE:", res.json())

# 6. READ all clients again to confirm deletion
res = requests.get(f"{BASE_URL}/clients/")
print("READ AFTER DELETE:", res.json())
