import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

orig_onSave = """                val s = initialSupplier ?: Supplier()
                onSave(s.copy(
                    name = name,
                    category = category,
                    description = description,
                    about = about,
                    basePrice = basePrice.toIntOrNull() ?: 0,
                    capacity = capacity.toIntOrNull() ?: 0,
                    location = location,
                    services = services
                ))"""

new_onSave = """                val s = initialSupplier ?: Supplier()
                onSave(s.copy(
                    name = name,
                    category = category,
                    description = description,
                    about = about,
                    basePrice = basePrice.toIntOrNull() ?: 0,
                    capacity = capacity.toIntOrNull() ?: 0,
                    location = location,
                    services = services
                ), selectedImages)"""

text = text.replace(orig_onSave, new_onSave)

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
