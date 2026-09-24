import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    content = f.read()

# Replace mockSuppliers with emptyList
content = content.replace("private val _suppliers = MutableStateFlow(mockSuppliers)", "private val _suppliers = MutableStateFlow<List<Supplier>>(emptyList())")

# Add fetchSuppliers to init block
init_block = """    init {
        fetchSuppliers()
        auth.currentUser?.let { user ->
            fetchUserFromFirestore(user.uid)
        }
    }

    private fun fetchSuppliers() {
        db.collection("suppliers").addSnapshotListener { snapshot, e ->
            if (e != null) return@addSnapshotListener
            val newSuppliers = snapshot?.documents?.mapNotNull { doc ->
                try {
                    doc.toObject(Supplier::class.java)
                } catch (e: Exception) { null }
            } ?: emptyList()
            _suppliers.value = newSuppliers
        }
    }"""
content = re.sub(r'    init \{.*?\n    \}', init_block, content, flags=re.DOTALL)

# Update authenticate to add a supplier document
auth_orig = """                    val userMap = hashMapOf(
                        "name" to name,
                        "email" to email,
                        "phone" to phone,
                        "role" to role
                    )
                    db.collection("users").document(uid).set(userMap).await()"""

auth_new = """                    val userMap = hashMapOf(
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
                    }"""
content = content.replace(auth_orig, auth_new)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(content)

