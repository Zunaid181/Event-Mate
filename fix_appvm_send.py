import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

# Using regex to replace the entire sendRequests function block
pattern = r"    fun sendRequests\(\) \{.*?(?=    fun updateRequestStatus)"
replacement = """    fun sendRequests() {
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
                } catch (e: Exception) {}
            }
        }
        _serviceRequests.value = _serviceRequests.value + newRequests
    }
"""

text = re.sub(pattern, replacement, text, flags=re.DOTALL)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
