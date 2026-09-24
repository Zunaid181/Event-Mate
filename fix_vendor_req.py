import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

orig = """                                if (req.status == RequestStatus.PENDING) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Button(onClick = { viewModel.updateRequestStatus(req.id, RequestStatus.ACCEPTED) }, modifier = Modifier.weight(1f)) {
                                            Icon(Icons.Default.Check, contentDescription = null)
                                            Spacer(Modifier.width(4.dp))
                                            Text("Accept")
                                        }
                                        OutlinedButton(onClick = { viewModel.updateRequestStatus(req.id, RequestStatus.REJECTED) }, modifier = Modifier.weight(1f)) {
                                            Icon(Icons.Default.Close, contentDescription = null)
                                            Spacer(Modifier.width(4.dp))
                                            Text("Reject")
                                        }
                                    }
                                } else {
                                    val color = if (req.status == RequestStatus.ACCEPTED) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error
                                    Text("Status: ${req.status.name}", color = color, fontWeight = FontWeight.Bold)
                                }"""

new = """                                if (req.editStatus == RequestStatus.PENDING) {
                                    Spacer(Modifier.height(8.dp))
                                    Text("Requested Changes:", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.tertiary)
                                    Text(req.editedPlanDetails ?: "", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.tertiary)
                                    Spacer(Modifier.height(8.dp))
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Button(onClick = { viewModel.updateEditStatus(req.id, RequestStatus.ACCEPTED) }, modifier = Modifier.weight(1f)) {
                                            Icon(Icons.Default.Check, contentDescription = null)
                                            Spacer(Modifier.width(4.dp))
                                            Text("Accept Edit")
                                        }
                                        OutlinedButton(onClick = { viewModel.updateEditStatus(req.id, RequestStatus.REJECTED) }, modifier = Modifier.weight(1f)) {
                                            Icon(Icons.Default.Close, contentDescription = null)
                                            Spacer(Modifier.width(4.dp))
                                            Text("Reject Edit")
                                        }
                                    }
                                } else if (req.status == RequestStatus.PENDING) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Button(onClick = { viewModel.updateRequestStatus(req.id, RequestStatus.ACCEPTED) }, modifier = Modifier.weight(1f)) {
                                            Icon(Icons.Default.Check, contentDescription = null)
                                            Spacer(Modifier.width(4.dp))
                                            Text("Accept")
                                        }
                                        OutlinedButton(onClick = { viewModel.updateRequestStatus(req.id, RequestStatus.REJECTED) }, modifier = Modifier.weight(1f)) {
                                            Icon(Icons.Default.Close, contentDescription = null)
                                            Spacer(Modifier.width(4.dp))
                                            Text("Reject")
                                        }
                                    }
                                } else {
                                    val color = if (req.status == RequestStatus.ACCEPTED) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error
                                    Text("Status: ${req.status.name}", color = color, fontWeight = FontWeight.Bold)
                                }"""

text = text.replace(orig, new)

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
