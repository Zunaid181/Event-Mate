with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

import re
text = re.sub(r'import androidx.activity.result.contract.ActivityResultContracts\nimport androidx.activity.result.contract.ActivityResultContracts\n', 'import androidx.activity.result.contract.ActivityResultContracts\n', text)
text = text.replace("import androidx.activity.result.contract.ActivityResultContracts\nimport androidx.activity.result.contract.ActivityResultContracts", "import androidx.activity.result.contract.ActivityResultContracts")

text = text.replace("val photoPickerLauncher = rememberLauncherForActivityResult", "val photoPickerLauncher = rememberLauncherForActivityResult")

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)

