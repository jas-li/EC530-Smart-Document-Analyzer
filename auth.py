from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
users = {
    "user": "password",
}

@auth.verify_password

def verify_password(username, password):
    if username in users and users[username] == password:
        return username
