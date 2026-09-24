with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

import re

# Add launcher inside SupplierDashboardContent
text = text.replace("val requests by viewModel.serviceRequests.collectAsState()",
"""val launcher = androidx.activity.compose.rememberLauncherForActivityResult(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia()) { uri -> if (uri != null) viewModel.uploadVendorImage(uri) }
    val requests by viewModel.serviceRequests.collectAsState()""")

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
