import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_status_defs = """    val venueStatus = MutableStateFlow(RequestStatus.NONE)
    val photographerStatus = MutableStateFlow(RequestStatus.NONE)
    val catererStatus = MutableStateFlow(RequestStatus.NONE)
    val entertainmentStatus = MutableStateFlow(RequestStatus.NONE)"""

new_status_defs = """    val venueStatus = combine(_serviceRequests, selectedVenueId) { reqs, id -> 
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
text = text.replace(orig_status_defs, new_status_defs)

text = text.replace("venueStatus.value = RequestStatus.PENDING", "")
text = text.replace("photographerStatus.value = RequestStatus.PENDING", "")
text = text.replace("catererStatus.value = RequestStatus.PENDING", "")
text = text.replace("entertainmentStatus.value = RequestStatus.PENDING", "")

text = text.replace("venueStatus.value = RequestStatus.NONE", "")
text = text.replace("photographerStatus.value = RequestStatus.NONE", "")
text = text.replace("catererStatus.value = RequestStatus.NONE", "")
text = text.replace("entertainmentStatus.value = RequestStatus.NONE", "")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
