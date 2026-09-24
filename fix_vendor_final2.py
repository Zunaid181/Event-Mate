with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

import re

# Add launcher back to the top of VendorDashboardScreen
text = text.replace("val suppliers by viewModel.suppliers.collectAsState()",
"""val launcher = rememberLauncherForActivityResult(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia()) { uri -> if (uri != null) viewModel.uploadVendorImage(uri) }
    val suppliers by viewModel.suppliers.collectAsState()""")

# In SupplierDashboardContent, remove it if it was added (it failed grep earlier, so maybe it wasn't)

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
