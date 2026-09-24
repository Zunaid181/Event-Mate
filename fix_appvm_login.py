import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_fetch = """                    val role = doc.getString("role") ?: "Planner"
                    val profileImageUrl = doc.getString("profileImageUrl") ?: ""
                    _currentUser.value = User(
                        id = uid,
                        name = name,
                        email = email,
                        phone = phone,
                        role = role,
                        isAdmin = role == "Admin",
                        profileImageUrl = profileImageUrl
                    )"""
new_fetch = """                    val role = doc.getString("role") ?: "Planner"
                    val profileImageUrl = doc.getString("profileImageUrl") ?: ""
                    val isSuspended = doc.getBoolean("isSuspended") ?: false
                    val isBanned = doc.getBoolean("isBanned") ?: false
                    val isAdmin = doc.getBoolean("isAdmin") ?: (role == "Admin")
                    _currentUser.value = User(
                        id = uid,
                        name = name,
                        email = email,
                        phone = phone,
                        role = role,
                        isAdmin = isAdmin,
                        profileImageUrl = profileImageUrl,
                        isSuspended = isSuspended,
                        isBanned = isBanned
                    )"""
text = text.replace(orig_fetch, new_fetch)

orig_signin = """                } else {
                    val res = auth.signInWithEmailAndPassword(email, pass).await()
                    val uid = res.user?.uid ?: throw Exception("Auth failed")
                    fetchUserFromFirestore(uid)
                    onResult(true, null)
                }"""
new_signin = """                } else {
                    val res = auth.signInWithEmailAndPassword(email, pass).await()
                    val uid = res.user?.uid ?: throw Exception("Auth failed")
                    
                    val doc = db.collection("users").document(uid).get().await()
                    val isSuspended = doc.getBoolean("isSuspended") ?: false
                    val isBanned = doc.getBoolean("isBanned") ?: false
                    if (isBanned) {
                        auth.signOut()
                        onResult(false, "This account has been banned.")
                        return@launch
                    }
                    if (isSuspended) {
                        auth.signOut()
                        onResult(false, "This account is currently suspended.")
                        return@launch
                    }
                    
                    fetchUserFromFirestore(uid)
                    onResult(true, null)
                }"""
text = text.replace(orig_signin, new_signin)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
