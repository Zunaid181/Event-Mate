import re

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "r") as f:
    text = f.read()

orig_filter = """        val isAvailable = isAdmin || (!dateConflict && !capacityConflict)
        
        isCategory && isSearch && isLocation && isAvailable"""

new_filter = """        val isAvailable = isAdmin || (!dateConflict && !capacityConflict)
        val isPub = isAdmin || it.isPublished
        
        isCategory && isSearch && isLocation && isAvailable && isPub"""

text = text.replace(orig_filter, new_filter)

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "w") as f:
    f.write(text)
