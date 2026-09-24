import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

new_methods = """
    fun sendEditRequest(requestId: String, newDetails: String) {
        viewModelScope.launch {
            try {
                val reqRef = db.collection("requests").document(requestId)
                db.batch().update(reqRef, "editedPlanDetails", newDetails, "editStatus", RequestStatus.PENDING).commit().await()
                _serviceRequests.value = _serviceRequests.value.map {
                    if (it.id == requestId) it.copy(editedPlanDetails = newDetails, editStatus = RequestStatus.PENDING) else it
                }
            } catch (e: Exception) {}
        }
    }
    
    fun updateEditStatus(requestId: String, newStatus: RequestStatus) {
        val request = _serviceRequests.value.find { it.id == requestId } ?: return
        viewModelScope.launch {
            try {
                val reqRef = db.collection("requests").document(requestId)
                val batch = db.batch()
                if (newStatus == RequestStatus.ACCEPTED) {
                    batch.update(reqRef, "planDetails", request.editedPlanDetails, "editedPlanDetails", null, "editStatus", RequestStatus.NONE)
                    batch.commit().await()
                    _serviceRequests.value = _serviceRequests.value.map {
                        if (it.id == requestId) it.copy(planDetails = request.editedPlanDetails ?: it.planDetails, editedPlanDetails = null, editStatus = RequestStatus.NONE) else it
                    }
                } else if (newStatus == RequestStatus.REJECTED) {
                    batch.update(reqRef, "editedPlanDetails", null, "editStatus", RequestStatus.NONE, "hasUnreadRejection", true)
                    batch.commit().await()
                    _serviceRequests.value = _serviceRequests.value.map {
                        if (it.id == requestId) it.copy(editedPlanDetails = null, editStatus = RequestStatus.NONE, hasUnreadRejection = true) else it
                    }
                }
            } catch(e: Exception){}
        }
    }
    
    fun dismissRejectionNotification(requestId: String) {
        viewModelScope.launch {
            try {
                db.collection("requests").document(requestId).update("hasUnreadRejection", false).await()
                _serviceRequests.value = _serviceRequests.value.map {
                    if (it.id == requestId) it.copy(hasUnreadRejection = false) else it
                }
            } catch(e: Exception){}
        }
    }
"""

text = text.replace("    fun updateRequestStatus", new_methods + "\n    fun updateRequestStatus")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
