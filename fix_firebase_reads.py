import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    content = f.read()

# Add listeners to init block
orig_init = """    init {
        fetchSuppliers()
        auth.currentUser?.let { user ->
            fetchUserFromFirestore(user.uid)
        }
    }"""

new_init = """    init {
        fetchSuppliers()
        fetchBookings()
        fetchRequests()
        auth.currentUser?.let { user ->
            fetchUserFromFirestore(user.uid)
        }
    }
    
    private fun fetchBookings() {
        db.collection("bookings").addSnapshotListener { snapshot, e ->
            if (e != null) return@addSnapshotListener
            val newBookings = snapshot?.documents?.mapNotNull { doc ->
                try {
                    doc.toObject(Booking::class.java)
                } catch (e: Exception) { null }
            } ?: emptyList()
            _bookings.value = newBookings
        }
    }
    
    private fun fetchRequests() {
        db.collection("requests").addSnapshotListener { snapshot, e ->
            if (e != null) return@addSnapshotListener
            val newReqs = snapshot?.documents?.mapNotNull { doc ->
                try {
                    doc.toObject(ServiceRequest::class.java)
                } catch (e: Exception) { null }
            } ?: emptyList()
            _serviceRequests.value = newReqs
        }
    }"""

content = content.replace(orig_init, new_init)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(content)
