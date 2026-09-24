import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

# We need to pass the photoPickerLauncher down to SupplierDashboardContent. Or since it's just an activity result launcher, we can create another one inside SupplierDashboardContent.

# 1. Remove the broken lambda
broken_launcher_call = "photoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia.ImageOnly))"
fixed_launcher_call = "launcher.launch(androidx.activity.result.PickVisualMediaRequest(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia.ImageOnly))"
text = text.replace(broken_launcher_call, fixed_launcher_call)

# 2. Add launcher inside SupplierDashboardContent
orig_sig = "fun SupplierDashboardContent(user: User, supplier: com.eventmate.ui.models.Supplier, viewModel: AppViewModel, paddingValues: PaddingValues) {\n    val requests by viewModel.serviceRequests.collectAsState()"
new_sig = "fun SupplierDashboardContent(user: User, supplier: com.eventmate.ui.models.Supplier, viewModel: AppViewModel, paddingValues: PaddingValues) {\n    val launcher = rememberLauncherForActivityResult(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia()) { uri -> if (uri != null) viewModel.uploadVendorImage(uri) }\n    val requests by viewModel.serviceRequests.collectAsState()"
text = text.replace(orig_sig, new_sig)

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
