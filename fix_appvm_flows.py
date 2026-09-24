import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_flows = """    val venueStatus = combine(_serviceRequests, selectedVenueId) { reqs, id -> 
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

new_flows = """    val venueRequest = combine(_serviceRequests, selectedVenueId) { reqs, id -> 
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

text = text.replace(orig_flows, new_flows)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
