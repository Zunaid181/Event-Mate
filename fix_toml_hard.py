with open("gradle/libs.versions.toml", "r") as f:
    lines = f.readlines()

out = []
in_plugins = False
for line in lines:
    if "[plugins]" in line:
        in_plugins = True
    if in_plugins and ("firebase-storage =" in line or "firebase-messaging =" in line or "coil-compose =" in line):
        continue
    out.append(line)

with open("gradle/libs.versions.toml", "w") as f:
    f.writelines(out)
