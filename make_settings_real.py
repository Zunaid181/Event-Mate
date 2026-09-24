import re
with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "r") as f:
    text = f.read()

text = text.replace("import androidx.compose.ui.layout.ContentScale", "import androidx.compose.ui.layout.ContentScale\nimport androidx.compose.material3.Switch")

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(text)
