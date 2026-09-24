import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

orig_dialog = """@Composable
fun ManageAvailabilityDialog(
    supplier: Supplier,
    onDismiss: () -> Unit,
    onToggleDate: (String) -> Unit
) {
    var dateInput by remember { mutableStateOf("") }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Manage Availability") },
        text = {
            Column {
                Text("Select dates to mark as UNAVAILABLE:")
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = dateInput,
                    onValueChange = { dateInput = it },
                    label = { Text("YYYY-MM-DD") },
                    modifier = Modifier.fillMaxWidth()
                )
                Button(onClick = { 
                    if (dateInput.isNotEmpty()) {
                        onToggleDate(dateInput)
                        dateInput = ""
                    }
                }, modifier = Modifier.align(Alignment.End).padding(top=8.dp)) {
                    Text("Add Date")
                }
                
                Spacer(Modifier.height(16.dp))
                Text("Unavailable Dates:", fontWeight = FontWeight.Bold)
                LazyColumn(modifier = Modifier.heightIn(max = 200.dp)) {
                    items(supplier.bookedDates) { d ->
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                            Text(d)
                            IconButton(onClick = { onToggleDate(d) }) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove")
                            }
                        }
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) { Text("Done") }
        }
    )
}"""

new_dialog = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ManageAvailabilityDialog(
    supplier: Supplier,
    onDismiss: () -> Unit,
    onToggleDate: (String) -> Unit
) {
    var showDatePicker by remember { mutableStateOf(false) }
    val datePickerState = rememberDatePickerState()
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Manage Availability") },
        text = {
            Column {
                Text("Select dates to mark as UNAVAILABLE:")
                Spacer(Modifier.height(8.dp))
                
                Button(onClick = { showDatePicker = true }, modifier = Modifier.fillMaxWidth()) {
                    Icon(Icons.Default.DateRange, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                    Text("Pick a Date")
                }
                
                Spacer(Modifier.height(16.dp))
                Text("Unavailable Dates:", fontWeight = FontWeight.Bold)
                LazyColumn(modifier = Modifier.heightIn(max = 200.dp)) {
                    items(supplier.bookedDates) { d ->
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                            Text(d)
                            IconButton(onClick = { onToggleDate(d) }) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove")
                            }
                        }
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) { Text("Done") }
        }
    )
    
    if (showDatePicker) {
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(onClick = {
                    datePickerState.selectedDateMillis?.let { millis ->
                        val cal = java.util.Calendar.getInstance()
                        cal.timeInMillis = millis
                        val y = cal.get(java.util.Calendar.YEAR)
                        val m = cal.get(java.util.Calendar.MONTH) + 1
                        val d = cal.get(java.util.Calendar.DAY_OF_MONTH)
                        val dateStr = String.format("%04d-%02d-%02d", y, m, d)
                        onToggleDate(dateStr)
                    }
                    showDatePicker = false
                }) { Text("OK") }
            },
            dismissButton = {
                TextButton(onClick = { showDatePicker = false }) { Text("Cancel") }
            }
        ) {
            DatePicker(state = datePickerState)
        }
    }
}"""
text = text.replace(orig_dialog, new_dialog)
with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
