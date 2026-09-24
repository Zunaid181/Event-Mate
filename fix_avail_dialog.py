import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

orig_dialog_call = """    if (showAvailabilityDialog != null) {
        ManageAvailabilityDialog(
            supplier = showAvailabilityDialog!!,
            onDismiss = { showAvailabilityDialog = null },
            onToggleDate = { date -> viewModel.toggleSupplierDate(showAvailabilityDialog!!.id, date) }
        )
    }"""

new_dialog_call = """    if (showAvailabilityDialog != null) {
        val currentSupplier = suppliers.find { it.id == showAvailabilityDialog!!.id } ?: showAvailabilityDialog!!
        ManageAvailabilityDialog(
            supplier = currentSupplier,
            onDismiss = { showAvailabilityDialog = null },
            onToggleDate = { date -> viewModel.toggleSupplierDate(currentSupplier.id, date) }
        )
    }"""

text = text.replace(orig_dialog_call, new_dialog_call)

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
