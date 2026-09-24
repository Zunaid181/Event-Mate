import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

text = text.replace("photoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))", 
                    "photoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia.ImageOnly))")

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
