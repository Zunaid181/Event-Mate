import re

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "r") as f:
    text = f.read()

orig_filter = "val vendors = viewModel.suppliers.collectAsState().value"
new_filter = "val allSuppliers = viewModel.suppliers.collectAsState().value\n    val vendors = allSuppliers.filter { it.isPublished && it.vendorId != currentUser?.id }"

text = text.replace(orig_filter, new_filter)
# Just in case the collectAsState() happens elsewhere:
text = text.replace("val suppliers by viewModel.suppliers.collectAsState()", "val allSuppliers by viewModel.suppliers.collectAsState()\n    val suppliers = allSuppliers.filter { it.isPublished && it.vendorId != currentUser?.id }")

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "w") as f:
    f.write(text)
