with open("gradle/libs.versions.toml", "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    if "firebase-storage2 =" in line:
        continue
    out.append(line)

with open("gradle/libs.versions.toml", "w") as f:
    f.writelines(out)
