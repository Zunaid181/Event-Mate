import re

with open("app/src/main/java/com/eventmate/ui/screens/PlanningScreen.kt", "r") as f:
    text = f.read()

text = text.replace("editDetails = request.planDetails", "editDetails = request?.planDetails ?: \"\"")

with open("app/src/main/java/com/eventmate/ui/screens/PlanningScreen.kt", "w") as f:
    f.write(text)
