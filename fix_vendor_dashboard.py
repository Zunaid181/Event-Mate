import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    content = f.read()

imports = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
"""
content = content.replace("import com.eventmate.ui.viewmodels.AppViewModel", imports + "\nimport com.eventmate.ui.viewmodels.AppViewModel")

launcher = """@Composable
fun VendorDashboardScreen(
    viewModel: AppViewModel,
    currentUser: User?,
    onNavigateToHome: () -> Unit,
    onNavigateToPlanning: () -> Unit,
    onNavigateToProfile: () -> Unit
) {
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri ->
            if (uri != null) {
                viewModel.uploadVendorImage(uri)
            }
        }
    )"""
content = content.replace("""@Composable
fun VendorDashboardScreen(
    viewModel: AppViewModel,
    currentUser: User?,
    onNavigateToHome: () -> Unit,
    onNavigateToPlanning: () -> Unit,
    onNavigateToProfile: () -> Unit
) {""", launcher)

orig_btn = """                    Button(onClick = {}, modifier = Modifier.fillMaxWidth()) { Text("Edit Profile & Services") }"""
new_btn = """                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = {}, modifier = Modifier.weight(1f)) { Text("Edit Profile & Services") }
                        OutlinedButton(
                            onClick = { photoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) },
                            modifier = Modifier.weight(1f)
                        ) { Text("Upload Cover Photo") }
                    }"""
content = content.replace(orig_btn, new_btn)

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(content)
