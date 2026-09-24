import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig = """    fun toggleSupplierDate(supplierId: String, date: String) {
        _suppliers.value = _suppliers.value.map {
            if (it.id == supplierId) {
                val updatedDates = if (date in it.bookedDates) it.bookedDates - date else it.bookedDates + date
                it.copy(bookedDates = updatedDates)
            } else it
        }
    }"""

new = """    fun toggleSupplierDate(supplierId: String, date: String) {
        val supplier = _suppliers.value.find { it.id == supplierId } ?: return
        val updatedDates = if (date in supplier.bookedDates) supplier.bookedDates - date else supplier.bookedDates + date
        viewModelScope.launch {
            try {
                db.collection("suppliers").document(supplierId).update("bookedDates", updatedDates).await()
            } catch (e: Exception) {}
        }
    }"""

text = text.replace(orig, new)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
