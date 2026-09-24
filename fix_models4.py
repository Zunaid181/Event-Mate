import re

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "r") as f:
    content = f.read()

content = re.sub(r'val mockSuppliers = listOf\(.*?\)\)', '', content, flags=re.DOTALL)
content = content.replace("    Supplier(", "")
content = content.replace("            SupplierService(", "")

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "w") as f:
    f.write(content)
