import re
with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "r") as f:
    text = f.read()

# Make settings functional or just provide UI structure for it
text = text.replace("Text(\"Theme (Dark/Light)\")", "Text(\"Theme (Dark/Light)\"); Spacer(Modifier.weight(1f)); Switch(checked = true, onCheckedChange = {})")
text = text.replace("Text(\"Notifications\")", "Text(\"Notifications\"); Spacer(Modifier.weight(1f)); Switch(checked = true, onCheckedChange = {})")
text = text.replace("Text(\"Offline Caching\")", "Text(\"Offline Caching\"); Spacer(Modifier.weight(1f)); Switch(checked = true, onCheckedChange = {})")

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(text)
