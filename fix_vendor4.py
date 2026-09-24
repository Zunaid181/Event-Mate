with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

import re
text = re.sub(r'import androidx.activity.result.contract.ActivityResultContracts\nimport androidx.activity.result.contract.ActivityResultContracts', 'import androidx.activity.result.contract.ActivityResultContracts', text)

text = text.replace("photoPickerLauncher.launch", "viewModel.uploadVendorImage(android.net.Uri.EMPTY)")

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
