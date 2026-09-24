import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_fetch = """                            val category = doc.getString("category") ?: ""
                            val date = doc.getString("date") ?: ""
                            val guestCount = doc.getLong("guestCount")?.toInt() ?: 0
                            val planDetails = doc.getString("planDetails") ?: ""
                            val statusStr = doc.getString("status") ?: "PENDING"
                            val status = try { RequestStatus.valueOf(statusStr) } catch (e: Exception) { RequestStatus.PENDING }"""

new_fetch = """                            val category = doc.getString("category") ?: ""
                            val date = doc.getString("date") ?: ""
                            val guestCount = doc.getLong("guestCount")?.toInt() ?: 0
                            val planDetails = doc.getString("planDetails") ?: ""
                            val statusStr = doc.getString("status") ?: "PENDING"
                            val status = try { RequestStatus.valueOf(statusStr) } catch (e: Exception) { RequestStatus.PENDING }
                            
                            val editedPlanDetails = doc.getString("editedPlanDetails")
                            val editStatusStr = doc.getString("editStatus") ?: "NONE"
                            val editStatus = try { RequestStatus.valueOf(editStatusStr) } catch(e: Exception) { RequestStatus.NONE }
                            val hasUnreadRejection = doc.getBoolean("hasUnreadRejection") ?: false"""

text = text.replace(orig_fetch, new_fetch)

orig_service_req = """                            ServiceRequest(id, plannerId, plannerName, plannerPhone, plannerEmail, supplierId, vendorId, category, date, guestCount, planDetails, status)"""
new_service_req = """                            ServiceRequest(id, plannerId, plannerName, plannerPhone, plannerEmail, supplierId, vendorId, category, date, guestCount, planDetails, status, editedPlanDetails, editStatus, hasUnreadRejection)"""

text = text.replace(orig_service_req, new_service_req)

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
