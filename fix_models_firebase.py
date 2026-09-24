import re

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "r") as f:
    content = f.read()

content = content.replace("data class Booking(", "data class Booking(\n    val id: String = \"\",")
content = content.replace("    val id: String,\n", "", 1) # First occurrence only

content = content.replace("data class ServiceRequest(", "data class ServiceRequest(\n    val id: String = \"\",\n    val plannerName: String = \"\",\n    val supplierId: String = \"\",\n    val category: String = \"\",\n    val date: String = \"\",\n    val guestCount: Int = 0,")
content = re.sub(r'    val id: String,\n    val plannerName: String,\n    val supplierId: String,\n    val category: String,\n    val date: String,\n    val guestCount: Int,\n', '', content)

content = content.replace("val plannerName: String,", "val plannerName: String = \"\",")
content = content.replace("val date: String,", "val date: String = \"\",")
content = content.replace("val guestCount: Int,", "val guestCount: Int = 0,")
content = content.replace("val venueName: String?,", "val venueName: String? = null,")
content = content.replace("val photographerName: String?,", "val photographerName: String? = null,")
content = content.replace("val catererName: String?,", "val catererName: String? = null,")
content = content.replace("val entertainmentName: String?,", "val entertainmentName: String? = null,")
content = content.replace("val totalCost: Int", "val totalCost: Int = 0")


with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "w") as f:
    f.write(content)
