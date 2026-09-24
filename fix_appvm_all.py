import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

# 1. Move the `combine` variables down.
combine_str = """    val venueStatus = combine(_serviceRequests, selectedVenueId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }?.status ?: RequestStatus.NONE 
    }.stateIn(viewModelScope, SharingStarted.Lazily, RequestStatus.NONE)
    val photographerStatus = combine(_serviceRequests, selectedPhotographerId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }?.status ?: RequestStatus.NONE 
    }.stateIn(viewModelScope, SharingStarted.Lazily, RequestStatus.NONE)
    val catererStatus = combine(_serviceRequests, selectedCatererId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }?.status ?: RequestStatus.NONE 
    }.stateIn(viewModelScope, SharingStarted.Lazily, RequestStatus.NONE)
    val entertainmentStatus = combine(_serviceRequests, selectedEntertainmentId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }?.status ?: RequestStatus.NONE 
    }.stateIn(viewModelScope, SharingStarted.Lazily, RequestStatus.NONE)"""

text = text.replace(combine_str, "")

# Insert it after `val entertainmentSelectedServices`
insert_target = "val entertainmentSelectedServices = MutableStateFlow<Set<String>>(emptySet())"
text = text.replace(insert_target, insert_target + "\n" + combine_str)


# 2. Fix sendRequests()
old_send = """    fun sendRequests() {
        val plannerName = currentUser.value?.name ?: "Planner"
        val d = eventDate.value ?: return
        val g = expectedGuestCount.value ?: 0
        val newRequests = mutableListOf<ServiceRequest>()
        if (selectedVenueId.value != null && venueStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedVenueId.value!!, "Venue", d, g))
            
        }
        if (selectedPhotographerId.value != null && photographerStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedPhotographerId.value!!, "Photographer", d, g))
            
        }
        if (selectedCatererId.value != null && catererStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedCatererId.value!!, "Caterer", d, g))
            
        }
        if (selectedEntertainmentId.value != null && entertainmentStatus.value == RequestStatus.NONE) {
            newRequests.add(ServiceRequest(UUID.randomUUID().toString(), plannerName, selectedEntertainmentId.value!!, "Entertainment", d, g))
            
        }
        viewModelScope.launch {
            newRequests.forEach { req ->
                try {
                    db.collection("requests").document(req.id).set(req).await()
                } catch (e: Exception) {
                    // Handle error
                }
            }
        }
        _serviceRequests.value = _serviceRequests.value + newRequests
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
        }
        createReq(selectedPhotographerId.value, photographerStatus.value, "Photographer", photographerSelectedServices.value)?.let { 
            newRequests.add(it)
        }
        createReq(selectedCatererId.value, catererStatus.value, "Caterer", catererSelectedServices.value)?.let { 
            newRequests.add(it)
        }
        createReq(selectedEntertainmentId.value, entertainmentStatus.value, "Entertainment", entertainmentSelectedServices.value)?.let { 
            newRequests.add(it)
        }
        viewModelScope.launch {
            newRequests.forEach { req ->
                try {
                    db.collection("requests").document(req.id).set(req).await()
                } catch (e: Exception) {
                    // Handle error
                }
            }
        }
        _serviceRequests.value = _serviceRequests.value + newRequests
    }"""
text = text.replace(old_send, new_send)


# 3. Remove re-assignments of venueStatus in updateRequestStatus
bad_status_assignments = """        if (request.supplierId == selectedVenueId.value) venueStatus.value = newStatus
        if (request.supplierId == selectedPhotographerId.value) photographerStatus.value = newStatus
        if (request.supplierId == selectedCatererId.value) catererStatus.value = newStatus
        if (request.supplierId == selectedEntertainmentId.value) entertainmentStatus.value = newStatus"""
text = text.replace(bad_status_assignments, "")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
