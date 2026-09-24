import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

orig_dialog_sig = """fun AddEditSupplierDialog(
    initialSupplier: Supplier?,
    currentUser: User?,
    onDismiss: () -> Unit,
    onSave: (Supplier) -> Unit
) {"""
new_dialog_sig = """fun AddEditSupplierDialog(
    initialSupplier: Supplier?,
    currentUser: User?,
    onDismiss: () -> Unit,
    onSave: (Supplier, List<android.net.Uri>) -> Unit
) {"""
text = text.replace(orig_dialog_sig, new_dialog_sig)

orig_dialog_vars = """    var location by remember { mutableStateOf(initialSupplier?.location ?: "") }
    
    // Add Services
    var newServiceName by remember { mutableStateOf("") }
    var newServicePrice by remember { mutableStateOf("") }
    var services by remember { mutableStateOf(initialSupplier?.services ?: emptyList()) }

    AlertDialog("""
new_dialog_vars = """    var location by remember { mutableStateOf(initialSupplier?.location ?: "") }
    
    // Add Services
    var newServiceName by remember { mutableStateOf("") }
    var newServicePrice by remember { mutableStateOf("") }
    var services by remember { mutableStateOf(initialSupplier?.services ?: emptyList()) }
    
    var selectedImages by remember { mutableStateOf<List<android.net.Uri>>(emptyList()) }
    val multiplePhotoPickerLauncher = rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.PickMultipleVisualMedia(),
        onResult = { uris -> selectedImages = uris }
    )

    AlertDialog("""
text = text.replace(orig_dialog_vars, new_dialog_vars)

orig_dialog_fields = """                    Spacer(Modifier.height(16.dp))
                    Text("Services", fontWeight = FontWeight.Bold)
                }
                items(services) { svc ->"""
new_dialog_fields = """                    Spacer(Modifier.height(16.dp))
                    Text("Images", fontWeight = FontWeight.Bold)
                    Button(onClick = { multiplePhotoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia.ImageOnly)) }) {
                        Text("Select Images")
                    }
                    if (selectedImages.isNotEmpty()) {
                        Text("${selectedImages.size} images selected", style = MaterialTheme.typography.bodySmall)
                    } else if (!initialSupplier?.imageUrls.isNullOrEmpty()) {
                        Text("${initialSupplier!!.imageUrls.size} images currently uploaded", style = MaterialTheme.typography.bodySmall)
                    }
                    
                    Spacer(Modifier.height(16.dp))
                    Text("Services", fontWeight = FontWeight.Bold)
                }
                items(services) { svc ->"""
text = text.replace(orig_dialog_fields, new_dialog_fields)

orig_save_btn = """            Button(onClick = {
                onSave(Supplier(
                    id = initialSupplier?.id ?: "",
                    vendorId = initialSupplier?.vendorId ?: "",
                    name = name,
                    category = category,
                    basePrice = basePrice.toIntOrNull() ?: 0,
                    capacity = capacity.toIntOrNull() ?: 0,
                    location = location,
                    description = description,
                    about = about,
                    services = services,
                    imageUrl = initialSupplier?.imageUrl ?: "",
                    isPublished = initialSupplier?.isPublished ?: false,
                    bookedDates = initialSupplier?.bookedDates ?: emptyList(),
                    rating = initialSupplier?.rating ?: 0.0,
                    reviewCount = initialSupplier?.reviewCount ?: 0,
                    maxCapacity = capacity.toIntOrNull()
                ))
            })"""
new_save_btn = """            Button(onClick = {
                onSave(Supplier(
                    id = initialSupplier?.id ?: "",
                    vendorId = initialSupplier?.vendorId ?: "",
                    name = name,
                    category = category,
                    basePrice = basePrice.toIntOrNull() ?: 0,
                    capacity = capacity.toIntOrNull() ?: 0,
                    location = location,
                    description = description,
                    about = about,
                    services = services,
                    imageUrl = initialSupplier?.imageUrl ?: "",
                    imageUrls = initialSupplier?.imageUrls ?: emptyList(),
                    isPublished = initialSupplier?.isPublished ?: false,
                    bookedDates = initialSupplier?.bookedDates ?: emptyList(),
                    rating = initialSupplier?.rating ?: 0.0,
                    reviewCount = initialSupplier?.reviewCount ?: 0,
                    maxCapacity = capacity.toIntOrNull()
                ), selectedImages)
            })"""
text = text.replace(orig_save_btn, new_save_btn)

orig_dashboard_save = """        AddEditSupplierDialog(
            initialSupplier = editingSupplier,
            currentUser = currentUser,
            onDismiss = { showAddDialog = false },
            onSave = { supplier ->
                viewModel.saveSupplier(supplier)
                showAddDialog = false
            }
        )"""
new_dashboard_save = """        AddEditSupplierDialog(
            initialSupplier = editingSupplier,
            currentUser = currentUser,
            onDismiss = { showAddDialog = false },
            onSave = { supplier, uris ->
                if (uris.isNotEmpty()) {
                    viewModel.saveSupplierWithImages(supplier, uris)
                } else {
                    viewModel.saveSupplier(supplier)
                }
                showAddDialog = false
            }
        )"""
text = text.replace(orig_dashboard_save, new_dashboard_save)

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)
