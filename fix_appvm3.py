with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

# Let's cleanly fix the brackets
# We know toggleSupplierDate ends, then there are brackets closing the class.
text = text.replace("    fun toggleSupplierDate(supplierId: String, date: String) {\n        _suppliers.value = _suppliers.value.map {\n            if (it.id == supplierId) {\n                val updatedDates = if (date in it.bookedDates) it.bookedDates - date else it.bookedDates + date\n                it.copy(bookedDates = updatedDates)\n            } else it\n        }\n    }\n}\n    fun uploadProfileImage", "    fun toggleSupplierDate(supplierId: String, date: String) {\n        _suppliers.value = _suppliers.value.map {\n            if (it.id == supplierId) {\n                val updatedDates = if (date in it.bookedDates) it.bookedDates - date else it.bookedDates + date\n                it.copy(bookedDates = updatedDates)\n            } else it\n        }\n    }\n    fun uploadProfileImage")

# If there is another stray } before uploadProfileImage
text = text.replace("    }\n}\n    fun uploadProfileImage", "    }\n    fun uploadProfileImage")
text = text.replace("    }\n}\n}\n    fun uploadProfileImage", "    }\n    fun uploadProfileImage")

# Just to be safe, I'll use regex to remove any } before uploadProfileImage
import re
text = re.sub(r'\}\s+fun uploadProfileImage', '} \n    fun uploadProfileImage', text)
text = re.sub(r'\}\s+\}\s+fun uploadProfileImage', '}\n    fun uploadProfileImage', text)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
