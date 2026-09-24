with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

funcs = """
    fun loadAllUsers() {
        viewModelScope.launch {
            try {
                db.collection("users").addSnapshotListener { snapshot, _ ->
                    if (snapshot != null) {
                        _allUsers.value = snapshot.toObjects(User::class.java)
                    }
                }
            } catch (e: Exception) {}
        }
    }
    
    fun updateUserStatus(userId: String, isSuspended: Boolean, isBanned: Boolean, isAdmin: Boolean) {
        viewModelScope.launch {
            try {
                db.collection("users").document(userId).update(
                    mapOf(
                        "isSuspended" to isSuspended,
                        "isBanned" to isBanned,
                        "isAdmin" to isAdmin
                    )
                ).await()
            } catch (e: Exception) {}
        }
    }
}
"""

text = text.rstrip()
if text.endswith("}"):
    text = text[:-1] + funcs
    
with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
