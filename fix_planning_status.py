import re

with open("app/src/main/java/com/eventmate/ui/screens/PlanningScreen.kt", "r") as f:
    text = f.read()

text = text.replace("venueStatus", "(venueRequest?.status ?: com.eventmate.ui.models.RequestStatus.NONE)")
text = text.replace("photographerStatus", "(photographerRequest?.status ?: com.eventmate.ui.models.RequestStatus.NONE)")
text = text.replace("catererStatus", "(catererRequest?.status ?: com.eventmate.ui.models.RequestStatus.NONE)")
text = text.replace("entertainmentStatus", "(entertainmentRequest?.status ?: com.eventmate.ui.models.RequestStatus.NONE)")

with open("app/src/main/java/com/eventmate/ui/screens/PlanningScreen.kt", "w") as f:
    f.write(text)
