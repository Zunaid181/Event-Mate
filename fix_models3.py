import re

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "r") as f:
    content = f.read()

content = content.replace("    val id: String,\n    val plannerName: String = \"\",", "    val plannerName: String = \"\",")
content = re.sub(r'val mockSuppliers = listOf\(.*?\)\)', '', content, flags=re.DOTALL)
content = content.replace("data class User(\n    val name: String,", "data class User(\n    val id: String = \"\",\n    val name: String = \"\",")
content = content.replace("val email: String,", "val email: String = \"\",")
content = content.replace("val phone: String,", "val phone: String = \"\",")
content = content.replace("val role: String,", "val role: String = \"\",")
content = content.replace("val isAdmin: Boolean", "val isAdmin: Boolean = false")


with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "w") as f:
    f.write(content)
