import re

with open("gradle/libs.versions.toml", "r") as f:
    content = f.read()

# Add to libraries block
libs = """
firebase-storage = { group = "com.google.firebase", name = "firebase-storage" }
firebase-messaging = { group = "com.google.firebase", name = "firebase-messaging" }
coil-compose = { group = "io.coil-kt", name = "coil-compose", version = "2.4.0" }
[plugins]"""
content = content.replace("[plugins]", libs)

with open("gradle/libs.versions.toml", "w") as f:
    f.write(content)
