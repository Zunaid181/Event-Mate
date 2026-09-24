with open("gradle/libs.versions.toml", "r") as f:
    text = f.read()

# Replace the last [libraries] addition with proper insertion
text = text.replace("[libraries]\nfirebase-storage =", "firebase-storage2 =")

with open("gradle/libs.versions.toml", "w") as f:
    f.write(text)

