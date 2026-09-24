import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    content = f.read()

# Add storage imports
content = content.replace("import com.google.firebase.firestore.FirebaseFirestore", "import com.google.firebase.firestore.FirebaseFirestore\nimport com.google.firebase.firestore.FirebaseFirestoreSettings\nimport com.google.firebase.firestore.PersistentCacheSettings\nimport com.google.firebase.storage.FirebaseStorage\nimport android.net.Uri\nimport kotlinx.coroutines.Dispatchers\nimport kotlinx.coroutines.withContext")

# Initialize storage and offline caching
orig_init = """class AppViewModel : ViewModel() {
    private val auth = FirebaseAuth.getInstance()
    private val db = FirebaseFirestore.getInstance()"""

new_init = """class AppViewModel : ViewModel() {
    private val auth = FirebaseAuth.getInstance()
    private val db = FirebaseFirestore.getInstance().apply {
        firestoreSettings = FirebaseFirestoreSettings.Builder()
            .setLocalCacheSettings(PersistentCacheSettings.newBuilder().build())
            .build()
    }
    private val storage = FirebaseStorage.getInstance()"""
content = content.replace(orig_init, new_init)

# Faster Auth implementation - do concurrent writes
orig_auth = """                    val userMap = hashMapOf(
                        "name" to name,
                        "email" to email,
                        "phone" to phone,
                        "role" to role
                    )
                    db.collection("users").document(uid).set(userMap).await()
                    
                    if (role != "Planner" && role != "Admin") {
                        val supplierMap = Supplier(
                            id = uid,
                            name = name + " Services",
                            category = role,
                            basePrice = 500,
                            rating = 5.0,
                            reviewCount = 0,
                            imageUrl = "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&q=80&w=800",
                            description = "Welcome to my new $role business on Event Mate! Please contact me for details.",
                            services = listOf(SupplierService("Basic Package", 500), SupplierService("Premium Package", 1000)),
                            location = "Sydney, NSW",
                            capacity = 150,
                            bookedDates = emptyList(),
                            maxCapacity = 150
                        )
                        db.collection("suppliers").document(uid).set(supplierMap).await()
                    }
                    fetchUserFromFirestore(uid)"""

new_auth = """                    val userMap = hashMapOf(
                        "name" to name,
                        "email" to email,
                        "phone" to phone,
                        "role" to role
                    )
                    
                    val batch = db.batch()
                    val userRef = db.collection("users").document(uid)
                    batch.set(userRef, userMap)
                    
                    if (role != "Planner" && role != "Admin") {
                        val supplierRef = db.collection("suppliers").document(uid)
                        val supplierMap = Supplier(
                            id = uid,
                            name = name + " Services",
                            category = role,
                            basePrice = 500,
                            rating = 5.0,
                            reviewCount = 0,
                            imageUrl = "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&q=80&w=800",
                            description = "Welcome to my new $role business on Event Mate! Please contact me for details.",
                            services = listOf(SupplierService("Basic Package", 500), SupplierService("Premium Package", 1000)),
                            location = "Sydney, NSW",
                            capacity = 150,
                            bookedDates = emptyList(),
                            maxCapacity = 150
                        )
                        batch.set(supplierRef, supplierMap)
                    }
                    batch.commit().await()
                    
                    // Optimistic UI update
                    _currentUser.value = User(
                        id = uid,
                        name = name,
                        email = email,
                        phone = phone,
                        role = role,
                        isAdmin = role == "Admin",
                        profileImageUrl = ""
                    )"""
content = content.replace(orig_auth, new_auth)

# Add uploadProfileImage
add_funcs = """
    fun uploadProfileImage(uri: Uri) {
        val uid = auth.currentUser?.uid ?: return
        viewModelScope.launch {
            try {
                val ref = storage.reference.child("profile_images/${uid}.jpg")
                ref.putFile(uri).await()
                val downloadUrl = ref.downloadUrl.await().toString()
                
                db.collection("users").document(uid).update("profileImageUrl", downloadUrl).await()
                _currentUser.value = _currentUser.value?.copy(profileImageUrl = downloadUrl)
            } catch (e: Exception) {
                // Ignore error
            }
        }
    }
    
    fun uploadVendorImage(uri: Uri) {
        val uid = auth.currentUser?.uid ?: return
        viewModelScope.launch {
            try {
                val ref = storage.reference.child("vendor_images/${uid}_${UUID.randomUUID()}.jpg")
                ref.putFile(uri).await()
                val downloadUrl = ref.downloadUrl.await().toString()
                
                db.collection("suppliers").document(uid).update("imageUrl", downloadUrl).await()
            } catch (e: Exception) {
                // Ignore error
            }
        }
    }
"""
content = content + add_funcs

# Add profileImageUrl to fetchUserFromFirestore
fetch_orig = """                    _currentUser.value = User(
                        id = uid,
                        name = name,
                        email = email,
                        phone = phone,
                        role = role,
                        isAdmin = role == "Admin"
                    )"""
fetch_new = """                    val profileImageUrl = doc.getString("profileImageUrl") ?: ""
                    _currentUser.value = User(
                        id = uid,
                        name = name,
                        email = email,
                        phone = phone,
                        role = role,
                        isAdmin = role == "Admin",
                        profileImageUrl = profileImageUrl
                    )"""
content = content.replace(fetch_orig, fetch_new)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(content)

