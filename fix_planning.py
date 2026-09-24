import re

with open("app/src/main/java/com/eventmate/ui/screens/PlanningScreen.kt", "r") as f:
    text = f.read()

orig = """    val venueStatus by viewModel.venueStatus.collectAsState()
    val photographerStatus by viewModel.photographerStatus.collectAsState()
    val catererStatus by viewModel.catererStatus.collectAsState()
    val entertainmentStatus by viewModel.entertainmentStatus.collectAsState()"""
new = """    val venueRequest by viewModel.venueRequest.collectAsState()
    val photographerRequest by viewModel.photographerRequest.collectAsState()
    val catererRequest by viewModel.catererRequest.collectAsState()
    val entertainmentRequest by viewModel.entertainmentRequest.collectAsState()"""
text = text.replace(orig, new)

orig_cards = """            item {
                ChecklistCard(
                    title = "Book Venue",
                    selectedId = selectedVenueId,
                    status = venueStatus,
                    onClick = { validateAndNavigate("Venue") }
                )
            }
            item {
                ChecklistCard(
                    title = "Hire Photographer",
                    selectedId = selectedPhotographerId,
                    status = photographerStatus,
                    onClick = { validateAndNavigate("Photographer") }
                )
            }
            item {
                ChecklistCard(
                    title = "Hire Caterer",
                    selectedId = selectedCatererId,
                    status = catererStatus,
                    onClick = { validateAndNavigate("Caterer") }
                )
            }
            item {
                ChecklistCard(
                    title = "Book Entertainment",
                    selectedId = selectedEntertainmentId,
                    status = entertainmentStatus,
                    onClick = { validateAndNavigate("Entertainment") }
                )
            }"""
new_cards = """            item {
                ChecklistCard(
                    title = "Book Venue",
                    selectedId = selectedVenueId,
                    request = venueRequest,
                    onClick = { validateAndNavigate("Venue") },
                    onEdit = { newDetails -> venueRequest?.let { viewModel.sendEditRequest(it.id, newDetails) } },
                    onDismissRejection = { venueRequest?.let { viewModel.dismissRejectionNotification(it.id) } }
                )
            }
            item {
                ChecklistCard(
                    title = "Hire Photographer",
                    selectedId = selectedPhotographerId,
                    request = photographerRequest,
                    onClick = { validateAndNavigate("Photographer") },
                    onEdit = { newDetails -> photographerRequest?.let { viewModel.sendEditRequest(it.id, newDetails) } },
                    onDismissRejection = { photographerRequest?.let { viewModel.dismissRejectionNotification(it.id) } }
                )
            }
            item {
                ChecklistCard(
                    title = "Hire Caterer",
                    selectedId = selectedCatererId,
                    request = catererRequest,
                    onClick = { validateAndNavigate("Caterer") },
                    onEdit = { newDetails -> catererRequest?.let { viewModel.sendEditRequest(it.id, newDetails) } },
                    onDismissRejection = { catererRequest?.let { viewModel.dismissRejectionNotification(it.id) } }
                )
            }
            item {
                ChecklistCard(
                    title = "Book Entertainment",
                    selectedId = selectedEntertainmentId,
                    request = entertainmentRequest,
                    onClick = { validateAndNavigate("Entertainment") },
                    onEdit = { newDetails -> entertainmentRequest?.let { viewModel.sendEditRequest(it.id, newDetails) } },
                    onDismissRejection = { entertainmentRequest?.let { viewModel.dismissRejectionNotification(it.id) } }
                )
            }"""
text = text.replace(orig_cards, new_cards)

orig_checklist = """fun ChecklistCard(title: String, selectedId: String?, status: com.eventmate.ui.models.RequestStatus, onClick: () -> Unit) {
    val containerColor by animateColorAsState(
        targetValue = when (status) {
            com.eventmate.ui.models.RequestStatus.PENDING -> Color.Yellow.copy(alpha = 0.2f)
            com.eventmate.ui.models.RequestStatus.ACCEPTED -> Color.Green.copy(alpha = 0.2f)
            com.eventmate.ui.models.RequestStatus.REJECTED -> Color.Red.copy(alpha = 0.2f)
            else -> MaterialTheme.colorScheme.surfaceVariant
        },
        animationSpec = tween(500)
    )

    val statusText = when (status) {
        com.eventmate.ui.models.RequestStatus.PENDING -> "Request Pending..."
        com.eventmate.ui.models.RequestStatus.ACCEPTED -> "Accepted! Ready to book."
        com.eventmate.ui.models.RequestStatus.REJECTED -> "Rejected. Please choose another."
        else -> if (selectedId != null) "Selected! Ready to send request." else ""
    }

    Card(modifier = Modifier.fillMaxWidth().animateContentSize().clickable { onClick() }, colors = CardDefaults.cardColors(containerColor = containerColor)) {
        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = selectedId != null, onCheckedChange = null)
            Spacer(Modifier.width(8.dp))
            Column {
                Text(title, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold)
                if (statusText.isNotEmpty()) {
                    Text(statusText, style = MaterialTheme.typography.bodySmall)
                }
            }
        }
    }
}"""

new_checklist = """fun ChecklistCard(title: String, selectedId: String?, request: com.eventmate.ui.models.ServiceRequest?, onClick: () -> Unit, onEdit: (String) -> Unit, onDismissRejection: () -> Unit) {
    var showEditDialog by remember { mutableStateOf(false) }
    var editDetails by remember { mutableStateOf("") }
    
    val status = request?.status ?: com.eventmate.ui.models.RequestStatus.NONE
    val editStatus = request?.editStatus ?: com.eventmate.ui.models.RequestStatus.NONE
    
    val containerColor by animateColorAsState(
        targetValue = when (status) {
            com.eventmate.ui.models.RequestStatus.PENDING -> Color.Yellow.copy(alpha = 0.2f)
            com.eventmate.ui.models.RequestStatus.ACCEPTED -> Color.Green.copy(alpha = 0.2f)
            com.eventmate.ui.models.RequestStatus.REJECTED -> Color.Red.copy(alpha = 0.2f)
            else -> MaterialTheme.colorScheme.surfaceVariant
        },
        animationSpec = tween(500)
    )

    val statusText = when (status) {
        com.eventmate.ui.models.RequestStatus.PENDING -> "Request Pending..."
        com.eventmate.ui.models.RequestStatus.ACCEPTED -> "Accepted! Ready to book."
        com.eventmate.ui.models.RequestStatus.REJECTED -> "Rejected. Please choose another."
        else -> if (selectedId != null) "Selected! Ready to send request." else ""
    }

    Card(modifier = Modifier.fillMaxWidth().animateContentSize().clickable { onClick() }, colors = CardDefaults.cardColors(containerColor = containerColor)) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = selectedId != null, onCheckedChange = null)
                Spacer(Modifier.width(8.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(title, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold)
                    if (statusText.isNotEmpty()) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(statusText, style = MaterialTheme.typography.bodySmall)
                            if (editStatus == com.eventmate.ui.models.RequestStatus.PENDING) {
                                Spacer(Modifier.width(4.dp))
                                Icon(Icons.Default.Warning, contentDescription = "Edit Pending", tint = Color(0xFFFFA500), modifier = Modifier.size(16.dp))
                                Text(" (Edit Pending)", style = MaterialTheme.typography.labelSmall, color = Color(0xFFFFA500))
                            }
                        }
                    }
                }
            }
            if (status == com.eventmate.ui.models.RequestStatus.ACCEPTED && editStatus != com.eventmate.ui.models.RequestStatus.PENDING) {
                TextButton(onClick = { 
                    editDetails = request.planDetails
                    showEditDialog = true 
                }, modifier = Modifier.align(Alignment.End)) {
                    Text("Edit Request")
                }
            }
            if (request?.hasUnreadRejection == true) {
                Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer), modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
                    Row(modifier = Modifier.padding(8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("Your changed request was rejected.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onErrorContainer, modifier = Modifier.weight(1f))
                        TextButton(onClick = onDismissRejection) {
                            Text("Dismiss")
                        }
                    }
                }
            }
        }
    }
    
    if (showEditDialog) {
        AlertDialog(
            onDismissRequest = { showEditDialog = false },
            title = { Text("Edit Request Details") },
            text = {
                OutlinedTextField(
                    value = editDetails,
                    onValueChange = { editDetails = it },
                    label = { Text("Details (Services, Guests, etc.)") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3
                )
            },
            confirmButton = {
                Button(onClick = { 
                    onEdit(editDetails)
                    showEditDialog = false
                }) {
                    Text("Send")
                }
            },
            dismissButton = {
                OutlinedButton(onClick = { showEditDialog = false }) { Text("Cancel") }
            }
        )
    }
}"""
text = text.replace(orig_checklist, new_checklist)

with open("app/src/main/java/com/eventmate/ui/screens/PlanningScreen.kt", "w") as f:
    f.write(text)
