import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

# Update sendRequests
orig_send = """    fun sendRequests() {
        val plannerName = currentUser.value?.name ?: "Planner"
        val d = eventDate.value ?: return
        val g = expectedGuestCount.value ?: 0
        val newRequests = mutableListOf<ServiceRequest>()
        if (selectedVenueId.value != null && venueStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedVenueId.value!!, "Venue", d, g))
            venueStatus.value = RequestStatus.PENDING
        }
        if (selectedPhotographerId.value != null && photographerStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedPhotographerId.value!!, "Photographer", d, g))
            photographerStatus.value = RequestStatus.PENDING
        }
        if (selectedCatererId.value != null && catererStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedCatererId.value!!, "Caterer", d, g))
            catererStatus.value = RequestStatus.PENDING
        }
        if (selectedEntertainmentId.value != null && entertainmentStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedEntertainmentId.value!!, "Entertainment", d, g))
            entertainmentStatus.value = RequestStatus.PENDING
        }"""

new_send = """    fun sendRequests() {
        val planner = currentUser.value ?: return
        val d = eventDate.value ?: return
        val g = expectedGuestCount.value ?: 0
        val newRequests = mutableListOf<ServiceRequest>()
        
        fun createReq(suppId: String?, status: RequestStatus, cat: String, services: Set<String>): ServiceRequest? {
            if (suppId == null || status != RequestStatus.NONE) return null
            val supp = _suppliers.value.find { it.id == suppId } ?: return null
            val planDetails = "Requested Services: ${services.joinToString(", ")}"
            return ServiceRequest(
                id = UUID.randomUUID().toString(),
                plannerId = planner.id,
                plannerName = planner.name,
                plannerEmail = planner.email,
                plannerPhone = planner.phone,
                supplierId = suppId,
                vendorId = supp.vendorId,
                category = cat,
                date = d,
                guestCount = g,
                planDetails = planDetails,
                status = RequestStatus.PENDING
            )
        }
        
        createReq(selectedVenueId.value, venueStatus.value, "Venue", venueSelectedServices.value)?.let { 
            newRequests.add(it)
            venueStatus.value = RequestStatus.PENDING 
        }
        createReq(selectedPhotographerId.value, photographerStatus.value, "Photographer", photographerSelectedServices.value)?.let { 
            newRequests.add(it)
            photographerStatus.value = RequestStatus.PENDING 
        }
        createReq(selectedCatererId.value, catererStatus.value, "Caterer", catererSelectedServices.value)?.let { 
            newRequests.add(it)
            catererStatus.value = RequestStatus.PENDING 
        }
        createReq(selectedEntertainmentId.value, entertainmentStatus.value, "Entertainment", entertainmentSelectedServices.value)?.let { 
            newRequests.add(it)
            entertainmentStatus.value = RequestStatus.PENDING 
        }"""
text = text.replace(orig_send, new_send)


# updateRequestStatus
orig_status = """    fun updateRequestStatus(requestId: String, newStatus: RequestStatus) {
        val request = _serviceRequests.value.find { it.id == requestId } ?: return
        
        viewModelScope.launch {
            try {
                db.collection("requests").document(requestId).update("status", newStatus).await()
            } catch (e: Exception) {
                // Handle error
            }
        }
        _serviceRequests.value = _serviceRequests.value.map {
            if (it.id == requestId) it.copy(status = newStatus) else it
        }"""

new_status = """    fun updateRequestStatus(requestId: String, newStatus: RequestStatus) {
        val request = _serviceRequests.value.find { it.id == requestId } ?: return
        
        viewModelScope.launch {
            try {
                val batch = db.batch()
                val reqRef = db.collection("requests").document(requestId)
                batch.update(reqRef, "status", newStatus)
                
                if (newStatus == RequestStatus.ACCEPTED) {
                    val supplierRef = db.collection("suppliers").document(request.supplierId)
                    val supplier = _suppliers.value.find { it.id == request.supplierId }
                    if (supplier != null && !supplier.bookedDates.contains(request.date)) {
                        val newDates = supplier.bookedDates + request.date
                        batch.update(supplierRef, "bookedDates", newDates)
                    }
                }
                batch.commit().await()
                
                if (newStatus == RequestStatus.ACCEPTED) {
                    _suppliers.value = _suppliers.value.map {
                        if (it.id == request.supplierId && !it.bookedDates.contains(request.date)) {
                            it.copy(bookedDates = it.bookedDates + request.date)
                        } else it
                    }
                }
                
                _serviceRequests.value = _serviceRequests.value.map {
                    if (it.id == requestId) it.copy(status = newStatus) else it
                }
            } catch (e: Exception) {
                // Handle error
            }
        }"""
text = text.replace(orig_status, new_status)

# also add saveSupplier function
add_save = """    fun saveSupplier(supplier: Supplier) {
        viewModelScope.launch {
            try {
                val id = if (supplier.id.isEmpty()) UUID.randomUUID().toString() else supplier.id
                val finalSupplier = supplier.copy(id = id, vendorId = auth.currentUser?.uid ?: return@launch)
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
    
    fun deleteSupplier(supplierId: String) {
        viewModelScope.launch {
            try {
                db.collection("suppliers").document(supplierId).delete().await()
                _suppliers.value = _suppliers.value.filter { it.id != supplierId }
            } catch(e:Exception){}
        }
    }
    
    fun togglePublishSupplier(supplierId: String, isPublished: Boolean) {
        viewModelScope.launch {
            try {
                db.collection("suppliers").document(supplierId).update("isPublished", isPublished).await()
                _suppliers.value = _suppliers.value.map { if (it.id == supplierId) it.copy(isPublished = isPublished) else it }
            } catch(e:Exception){}
        }
    }
"""

text = text.replace("    fun updateSupplierCapacity", add_save + "    fun updateSupplierCapacity")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
