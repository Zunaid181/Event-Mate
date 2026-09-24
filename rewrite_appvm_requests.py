import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

# 1. Add active request ID state flows
orig_selections = """    val selectedVenueId = MutableStateFlow<String?>(null)
    val eventOccasion = MutableStateFlow("")
    val venueSelectedServices = MutableStateFlow<Set<String>>(emptySet())

    val selectedPhotographerId = MutableStateFlow<String?>(null)
    val photographerHours = MutableStateFlow(0)
    val photographerSelectedServices = MutableStateFlow<Set<String>>(emptySet())
    
    val selectedCatererId = MutableStateFlow<String?>(null)
    val selectedEntertainmentId = MutableStateFlow<String?>(null)
    val entertainmentHours = MutableStateFlow(0)
    val catererSelectedServices = MutableStateFlow<Set<String>>(emptySet())
    val entertainmentSelectedServices = MutableStateFlow<Set<String>>(emptySet())"""

new_selections = """    val selectedVenueId = MutableStateFlow<String?>(null)
    val activeVenueRequestId = MutableStateFlow<String?>(null)
    val eventOccasion = MutableStateFlow("")
    val venueSelectedServices = MutableStateFlow<Set<String>>(emptySet())

    val selectedPhotographerId = MutableStateFlow<String?>(null)
    val activePhotographerRequestId = MutableStateFlow<String?>(null)
    val photographerHours = MutableStateFlow(0)
    val photographerSelectedServices = MutableStateFlow<Set<String>>(emptySet())
    
    val selectedCatererId = MutableStateFlow<String?>(null)
    val activeCatererRequestId = MutableStateFlow<String?>(null)
    val selectedEntertainmentId = MutableStateFlow<String?>(null)
    val activeEntertainmentRequestId = MutableStateFlow<String?>(null)
    val entertainmentHours = MutableStateFlow(0)
    val catererSelectedServices = MutableStateFlow<Set<String>>(emptySet())
    val entertainmentSelectedServices = MutableStateFlow<Set<String>>(emptySet())"""
text = text.replace(orig_selections, new_selections)

# 2. Update combine functions for requests
orig_combines = """    val venueRequest = combine(_serviceRequests, selectedVenueId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val photographerRequest = combine(_serviceRequests, selectedPhotographerId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val catererRequest = combine(_serviceRequests, selectedCatererId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val entertainmentRequest = combine(_serviceRequests, selectedEntertainmentId) { reqs, id -> 
        reqs.find { it.supplierId == id && it.plannerId == auth.currentUser?.uid }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)"""

new_combines = """    val venueRequest = combine(_serviceRequests, activeVenueRequestId) { reqs, reqId -> 
        reqs.find { it.id == reqId }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val photographerRequest = combine(_serviceRequests, activePhotographerRequestId) { reqs, reqId -> 
        reqs.find { it.id == reqId }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val catererRequest = combine(_serviceRequests, activeCatererRequestId) { reqs, reqId -> 
        reqs.find { it.id == reqId }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val entertainmentRequest = combine(_serviceRequests, activeEntertainmentRequestId) { reqs, reqId -> 
        reqs.find { it.id == reqId }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)"""
text = text.replace(orig_combines, new_combines)

# 3. Update select functions
orig_selects = """    fun selectVenue(id: String, occasion: String, services: Set<String>) {
        selectedVenueId.value = id
        eventOccasion.value = occasion
        venueSelectedServices.value = services
        
    }

    fun selectPhotographer(id: String, hours: Int, services: Set<String>) {
        selectedPhotographerId.value = id
        photographerHours.value = hours
        photographerSelectedServices.value = services
    }

    fun selectCaterer(id: String, services: Set<String>) {
        selectedCatererId.value = id
        catererSelectedServices.value = services
    }

    fun selectEntertainment(id: String, hours: Int, services: Set<String>) {
        selectedEntertainmentId.value = id
        entertainmentHours.value = hours
        entertainmentSelectedServices.value = services
    }"""
new_selects = """    fun selectVenue(id: String, occasion: String, services: Set<String>) {
        selectedVenueId.value = id
        eventOccasion.value = occasion
        venueSelectedServices.value = services
        activeVenueRequestId.value = null
    }

    fun selectPhotographer(id: String, hours: Int, services: Set<String>) {
        selectedPhotographerId.value = id
        photographerHours.value = hours
        photographerSelectedServices.value = services
        activePhotographerRequestId.value = null
    }

    fun selectCaterer(id: String, services: Set<String>) {
        selectedCatererId.value = id
        catererSelectedServices.value = services
        activeCatererRequestId.value = null
    }

    fun selectEntertainment(id: String, hours: Int, services: Set<String>) {
        selectedEntertainmentId.value = id
        entertainmentHours.value = hours
        entertainmentSelectedServices.value = services
        activeEntertainmentRequestId.value = null
    }"""
text = text.replace(orig_selects, new_selects)

# 4. Update clearPlan
orig_clear = """    fun clearPlan() {
        eventDate.value = null
        expectedGuestCount.value = null
        totalBudget.value = null
        selectedVenueId.value = null
        selectedPhotographerId.value = null
        selectedCatererId.value = null
        selectedEntertainmentId.value = null
    }"""
new_clear = """    fun clearPlan() {
        eventDate.value = null
        expectedGuestCount.value = null
        totalBudget.value = null
        selectedVenueId.value = null
        selectedPhotographerId.value = null
        selectedCatererId.value = null
        selectedEntertainmentId.value = null
        activeVenueRequestId.value = null
        activePhotographerRequestId.value = null
        activeCatererRequestId.value = null
        activeEntertainmentRequestId.value = null
    }"""
text = text.replace(orig_clear, new_clear)

# 5. Update sendRequests
orig_sendReqs = """        createReq(selectedVenueId.value, venueRequest.value?.status ?: RequestStatus.NONE, "Venue", venueSelectedServices.value)?.let { 
            newRequests.add(it)
        }
        createReq(selectedPhotographerId.value, photographerRequest.value?.status ?: RequestStatus.NONE, "Photographer", photographerSelectedServices.value)?.let { 
            newRequests.add(it)
        }
        createReq(selectedCatererId.value, catererRequest.value?.status ?: RequestStatus.NONE, "Caterer", catererSelectedServices.value)?.let { 
            newRequests.add(it)
        }
        createReq(selectedEntertainmentId.value, entertainmentRequest.value?.status ?: RequestStatus.NONE, "Entertainment", entertainmentSelectedServices.value)?.let { 
            newRequests.add(it)
        }"""
new_sendReqs = """        createReq(selectedVenueId.value, venueRequest.value?.status ?: RequestStatus.NONE, "Venue", venueSelectedServices.value)?.let { 
            newRequests.add(it)
            activeVenueRequestId.value = it.id
        }
        createReq(selectedPhotographerId.value, photographerRequest.value?.status ?: RequestStatus.NONE, "Photographer", photographerSelectedServices.value)?.let { 
            newRequests.add(it)
            activePhotographerRequestId.value = it.id
        }
        createReq(selectedCatererId.value, catererRequest.value?.status ?: RequestStatus.NONE, "Caterer", catererSelectedServices.value)?.let { 
            newRequests.add(it)
            activeCatererRequestId.value = it.id
        }
        createReq(selectedEntertainmentId.value, entertainmentRequest.value?.status ?: RequestStatus.NONE, "Entertainment", entertainmentSelectedServices.value)?.let { 
            newRequests.add(it)
            activeEntertainmentRequestId.value = it.id
        }"""
text = text.replace(orig_sendReqs, new_sendReqs)

# 6. Update fetchRequests to restore active session!
orig_fetchReqs = """    private fun fetchRequests() {
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
new_fetchReqs = """    private fun fetchRequests() {
        db.collection("requests").addSnapshotListener { snapshot, e ->
            if (e != null) return@addSnapshotListener
            val newReqs = snapshot?.documents?.mapNotNull { doc ->
                try {
                    doc.toObject(ServiceRequest::class.java)
                } catch (e: Exception) { null }
            } ?: emptyList()
            _serviceRequests.value = newReqs
            
            val uid = auth.currentUser?.uid
            if (uid != null) {
                val myReqs = newReqs.filter { it.plannerId == uid }
                val pendingOrAccepted = myReqs.filter { it.status == RequestStatus.PENDING || it.status == RequestStatus.ACCEPTED }
                
                if (selectedVenueId.value == null && activeVenueRequestId.value == null) {
                    pendingOrAccepted.find { it.category == "Venue" }?.let {
                        selectedVenueId.value = it.supplierId
                        activeVenueRequestId.value = it.id
                    }
                }
                if (selectedPhotographerId.value == null && activePhotographerRequestId.value == null) {
                    pendingOrAccepted.find { it.category == "Photographer" }?.let {
                        selectedPhotographerId.value = it.supplierId
                        activePhotographerRequestId.value = it.id
                    }
                }
                if (selectedCatererId.value == null && activeCatererRequestId.value == null) {
                    pendingOrAccepted.find { it.category == "Caterer" }?.let {
                        selectedCatererId.value = it.supplierId
                        activeCatererRequestId.value = it.id
                    }
                }
                if (selectedEntertainmentId.value == null && activeEntertainmentRequestId.value == null) {
                    pendingOrAccepted.find { it.category == "Entertainment" }?.let {
                        selectedEntertainmentId.value = it.supplierId
                        activeEntertainmentRequestId.value = it.id
                    }
                }
            }
        }
    }"""
text = text.replace(orig_fetchReqs, new_fetchReqs)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
