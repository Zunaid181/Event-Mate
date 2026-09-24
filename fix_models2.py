import re

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "r") as f:
    content = f.read()

content = re.sub(r'val mockSuppliers = listOf\(.*?\)\)', '', content, flags=re.DOTALL)

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "w") as f:
    f.write(content)
