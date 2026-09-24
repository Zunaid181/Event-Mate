import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

# Instead of MutableStateFlow for statuses, let's just make them properties, or compute them on the fly.
# But `venueStatus` etc are accessed as StateFlows in the UI (or maybe as `.value`). Let's check how they are used.

