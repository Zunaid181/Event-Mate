import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    content = f.read()

# Fix confirmBooking to write to Firestore
orig_confirm = """        val booking = Booking(
            id = UUID.randomUUID().toString(),
            plannerName = plannerName,
            date = d,
            guestCount = g,
            venueName = v?.name,
            photographerName = p?.name,
            catererName = c?.name,
            entertainmentName = e?.name,
            totalCost = cost
        )
        
        _bookings.value = _bookings.value + booking"""

new_confirm = """        val bookingId = UUID.randomUUID().toString()
        val booking = Booking(
            id = bookingId,
            plannerName = plannerName,
            date = d,
            guestCount = g,
            venueName = v?.name,
            photographerName = p?.name,
            catererName = c?.name,
            entertainmentName = e?.name,
            totalCost = cost
        )
        
        viewModelScope.launch {
            try {
                db.collection("bookings").document(bookingId).set(booking).await()
            } catch (e: Exception) {
                // Handle error
            }
        }
        
        _bookings.value = _bookings.value + booking"""

content = content.replace(orig_confirm, new_confirm)

# Fix sendRequests to write to Firestore
orig_send = """        _serviceRequests.value = _serviceRequests.value + newRequests"""

new_send = """        viewModelScope.launch {
            newRequests.forEach { req ->
                try {
                    db.collection("requests").document(req.id).set(req).await()
                } catch (e: Exception) {
                    // Handle error
                }
            }
        }
        _serviceRequests.value = _serviceRequests.value + newRequests"""

content = content.replace(orig_send, new_send)

# Fix updateRequestStatus to write to Firestore
orig_status = """        _serviceRequests.value = _serviceRequests.value.map {
            if (it.id == requestId) it.copy(status = newStatus) else it
        }"""

new_status = """        viewModelScope.launch {
            try {
                db.collection("requests").document(requestId).update("status", newStatus).await()
            } catch (e: Exception) {
                // Handle error
            }
        }
        _serviceRequests.value = _serviceRequests.value.map {
            if (it.id == requestId) it.copy(status = newStatus) else it
        }"""

content = content.replace(orig_status, new_status)


with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(content)

