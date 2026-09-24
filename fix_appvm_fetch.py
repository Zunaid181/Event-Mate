import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_fetch2 = """                    val isAdmin = doc.getBoolean("isAdmin") ?: (role == "Admin")
                    _currentUser.value = User(
                        id = uid,"""
new_fetch2 = """                    val isAdmin = doc.getBoolean("isAdmin") ?: (role == "Admin")
                    if (isBanned || isSuspended) {
                        auth.signOut()
                        _currentUser.value = null
                        return@launch
                    }
                    _currentUser.value = User(
                        id = uid,"""

text = text.replace(orig_fetch2, new_fetch2)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
