import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

text = text.replace("venueStatus.value", "venueRequest.value?.status ?: RequestStatus.NONE")
text = text.replace("photographerStatus.value", "photographerRequest.value?.status ?: RequestStatus.NONE")
text = text.replace("catererStatus.value", "catererRequest.value?.status ?: RequestStatus.NONE")
text = text.replace("entertainmentStatus.value", "entertainmentRequest.value?.status ?: RequestStatus.NONE")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
