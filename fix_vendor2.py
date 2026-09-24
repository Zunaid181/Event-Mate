import re
with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

text = text.replace("contract = ActivityResultContracts.PickVisualMedia(),", 
                    "contract = androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia(),")
text = text.replace("import androidx.activity.compose.rememberLauncherForActivityResult", 
                    "import androidx.activity.compose.rememberLauncherForActivityResult\nimport androidx.activity.result.contract.ActivityResultContracts")

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
