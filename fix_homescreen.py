import re

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "r") as f:
    text = f.read()

orig_nav = """                if (currentUser?.role == "Planner" || currentUser?.role == "Admin") {"""

new_nav = """                if (currentUser?.role == "Planner") {"""

text = text.replace(orig_nav, new_nav)

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "w") as f:
    f.write(text)
