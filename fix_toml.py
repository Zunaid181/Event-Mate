import re
with open("gradle/libs.versions.toml", "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    if "firebase-storage =" in line or "firebase-messaging =" in line or "coil-compose =" in line:
        continue
    out.append(line)
with open("gradle/libs.versions.toml", "w") as f:
    f.writelines(out)
