import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase

# cred = credentials.Certificate({
#     "type": "service_account",
#     "project_id": "djangowololo",
#     "private_key_id": "3a8b0f0ee2b46b030f76501066f7ba073778bde1",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDLy4aDwrBjRMg+\nM01jm9AxNT1rWdlikfKduq/C2tssek2wS3+N5aYm7gQT5ekm1MKFJCrUIOtRnEvK\njxsO1n8clKHlpzcAp857Q785bmXps/3S+7Kn4Y4az1Z88kygOZNz7xLfYs+VR93r\nR1IZK1BW9DmvXkx8V5qU+m4WuL15DVERcKcva7tlSV0DnMF3L5013B1qsxaRZvXa\nPg1PDJ7cBB92FuZJcr7aAWv5MVohP3BGX6Ujql4d7xduF4oAXh4X7pidB2vyvJWY\nWwnfYOg65T2e5cqFkOHiZIc9fQo/SP5+/h3/K556uUraUEAN8mCDVgibNVEjeR+M\nEiVxXbh5AgMBAAECggEABMugmg3dHO7fx9/o6qa+VMQYEoQ6GmjNBNNhYqRH+0FS\n/eqe4SHF4b1gzO+QZ4yi2aNu2xA9vU1AVs88f6JCOjPQpfDj+VDZidq/n4w2m3PT\n7ZCk5PCoqX6Wvkiszynfq38VCnren9iBszE50DQN10f2qgbd5aChl28Xo1L8SWKB\nJer2UMpcXRlByhLfDC0v1Q0T2UMCcj6QenLEIr2MF80gopVXOSCM8WuY3EoRnXIY\nth6DN6febjJNs10Yr7PllpvMQLNnVyP0yhIY8ZUEEHO3o2EOEzx7sBOODxuxMstJ\n+JvWqn8WLzCBT47xXWGivXUBA12qP3EGKPxA0YDJQQKBgQD+I7+ZeMRj8JfZrMKY\nHDUo0OHYnM0QRea5TwXJ7649tjDACfUTdHoDwP1E2dF7VC7ktAtLnxIrNPg92rz2\nOZQlby1S6UaUXKbyHA4n9jZExjyUFScjRa0XqJq9bh2QmY/ugQn6hCuwvz5Dd+fo\nbo+yWi9Xcdoxx4xDeRDzELPRuQKBgQDNSW6yKVVp2PtSGwBnzoUrv6bjiA4J56W3\ncoxZ8rV/UtFe2Q5UUiftQbjipMqwgQp1v2dyVBYJcIJ/aESNdc5tBxCFYszO8lrK\nje+1vpfTFWiMeKKLOrvmMAljG+vygEUq/BjST5F8GQjGrGyhMR3kiFsXm6l/1OXE\nUDEZ2W98wQKBgGyx4XrEekq8VlYVW80vE1V3sYCx38r7+qh7MeCikIV4bPVVzOob\nQSxl2G0gNEZpRP0wPDyFtoGgUCQ0b+lnywMPv/TcLQG7dvPKKAvTdHaJytMTEQA3\nBsc9p6EpfZ+g7jx2GEx7Ryx7PyggGqIA15jSlbjyyv3LeSRKnYM4O5CRAoGAZ49E\n1YG+gfAhEJFoifWH/sLnCN9o3ZxLYBjcLsAeyUVZM7Th4q2zUKAYCdXCHnpqcW4G\nXImIuGhWnLlX49jrMtsefXuTAE8IeChUJeYpJyYkoMB2lzAg/AV9ps6+H46P1hho\n2Sekp+rlH3x6LHLftpsHAQjY4BDhfEBMFNM4x8ECgYB+FBabhZ1b4eXbRqrSOO56\n/qN6SiHUK829vk+GwaLPnhgLaSBka3IZ6TQFljdnNpx57O1UX3uimOdRXR3N2wqW\nNXMgA5HWFqRe18Fd6w+kuc4JzFfJelebkgwbE0Xq5gN9WbSvIZGqU0BGl1iG2Aml\nGxZyqFWHCRzvbDzuUZuz4g==\n-----END PRIVATE KEY-----\n",
#     "client_email": "firebase-adminsdk-fzv4o@djangowololo.iam.gserviceaccount.com",
#     "client_id": "115387568576516194019",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fzv4o%40djangowololo.iam.gserviceaccount.com"
# })
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# config = {
#     "apiKey": "AIzaSyAUMWshtmX7N6C_dwQ8NOiQWUajzlDmujQ",
#     "authDomain": "djangowololo.firebaseapp.com",
#     "databaseURL": "https://djangowololo.firebaseio.com",
#     "projectId": "djangowololo",
#     "storageBucket": "djangowololo.appspot.com",
#     "messagingSenderId": "261943117982"
#   }
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
def get_db():
    return 'not anymore'

def get_auth():
    return 'not anymore'