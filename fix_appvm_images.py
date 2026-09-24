import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

new_fn = """    fun saveSupplierWithImages(supplier: Supplier, uris: List<android.net.Uri>) {
        viewModelScope.launch {
            try {
                val id = if (supplier.id.isEmpty()) UUID.randomUUID().toString() else supplier.id
                val uploadedUrls = mutableListOf<String>()
                for (uri in uris) {
                    val ref = storage.reference.child("supplier_images/${UUID.randomUUID()}")
                    ref.putFile(uri).await()
                    uploadedUrls.add(ref.downloadUrl.await().toString())
                }
                
                val finalUrls = supplier.imageUrls + uploadedUrls
                val finalSupplier = supplier.copy(id = id, vendorId = auth.currentUser?.uid ?: return@launch, imageUrls = finalUrls, imageUrl = finalUrls.firstOrNull() ?: supplier.imageUrl)
                db.collection("suppliers").document(id).set(finalSupplier).await()
                
                val exists = _suppliers.value.any { it.id == id }
                if (exists) {
                    _suppliers.value = _suppliers.value.map { if (it.id == id) finalSupplier else it }
                } else {
                    _suppliers.value = _suppliers.value + finalSupplier
                }
            } catch (e: Exception) {}
        }
    }
    
    fun saveSupplier"""

text = text.replace("    fun saveSupplier", new_fn)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
