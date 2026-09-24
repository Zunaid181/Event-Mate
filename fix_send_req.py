import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_send = """    fun sendRequests() {
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
        }"""
text = text.replace(orig_send, new_send)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
