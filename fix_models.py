import re

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "r") as f:
    text = f.read()

orig_user = """data class User(
    val id: String = "",
    val name: String = "",
    val email: String = "",
    val phone: String = "",
    val role: String = "",
    val isAdmin: Boolean = false,
    val profileImageUrl: String = ""
)"""

new_user = """data class User(
    val id: String = "",
    val name: String = "",
    val email: String = "",
    val phone: String = "",
    val role: String = "",
    val isAdmin: Boolean = false,
    val profileImageUrl: String = "",
    val isSuspended: Boolean = false,
    val isBanned: Boolean = false
)"""

text = text.replace(orig_user, new_user)

with open("app/src/main/java/com/eventmate/ui/models/Models.kt", "w") as f:
    f.write(text)
