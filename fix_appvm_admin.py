import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_guests = """    private val _guests = MutableStateFlow<List<Guest>>(emptyList())
    val guests: StateFlow<List<Guest>> = _guests.asStateFlow()"""

new_guests = """    private val _guests = MutableStateFlow<List<Guest>>(emptyList())
    val guests: StateFlow<List<Guest>> = _guests.asStateFlow()
    
    private val _allUsers = MutableStateFlow<List<User>>(emptyList())
    val allUsers: StateFlow<List<User>> = _allUsers.asStateFlow()"""

text = text.replace(orig_guests, new_guests)

fetch_func = """    fun loadAllUsers() {
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
"""

text = text.replace("    fun getVendorRequests(): List<ServiceRequest> {", fetch_func + "\n    fun getVendorRequests(): List<ServiceRequest> {")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
