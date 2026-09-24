import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

# Add db instance inside the class body, seems it's missing or messed up
# Let's just do a clean replacement of the whole class start
text = text.replace("    private val auth = FirebaseAuth.getInstance()\n    private val db = FirebaseFirestore.getInstance().apply {\n        firestoreSettings = FirebaseFirestoreSettings.Builder()\n            .setLocalCacheSettings(PersistentCacheSettings.newBuilder().build())\n            .build()\n    }\n    private val storage = FirebaseStorage.getInstance()", 
"    private val auth = FirebaseAuth.getInstance()\n    private val db = FirebaseFirestore.getInstance().apply {\n        firestoreSettings = FirebaseFirestoreSettings.Builder()\n            .setLocalCacheSettings(PersistentCacheSettings.newBuilder().build())\n            .build()\n    }\n    private val storage = FirebaseStorage.getInstance()")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
