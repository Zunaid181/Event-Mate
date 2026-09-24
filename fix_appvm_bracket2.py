with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

text = text.replace("    fun toggleSupplierDate(supplierId: String, date: String) {\n        _suppliers.value = _suppliers.value.map {\n            if (it.id == supplierId) {\n                val updatedDates = if (date in it.bookedDates) it.bookedDates - date else it.bookedDates + date\n                it.copy(bookedDates = updatedDates)\n            } else it\n        }\n    }\n}\n    fun uploadProfileImage", "    fun toggleSupplierDate(supplierId: String, date: String) {\n        _suppliers.value = _suppliers.value.map {\n            if (it.id == supplierId) {\n                val updatedDates = if (date in it.bookedDates) it.bookedDates - date else it.bookedDates + date\n                it.copy(bookedDates = updatedDates)\n            } else it\n        }\n    }\n    fun uploadProfileImage")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)

