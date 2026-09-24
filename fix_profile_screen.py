import re

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import coil.compose.AsyncImage"""
content = content.replace("import com.eventmate.ui.models.User", imports + "\nimport com.eventmate.ui.models.User")

# Add upload function to params
content = content.replace("    user: User,", "    user: User,\n    onUploadProfileImage: (android.net.Uri) -> Unit = {},")

# Add launcher
launcher = """    var isEditing by remember { mutableStateOf(false) }
    
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri ->
            if (uri != null) {
                onUploadProfileImage(uri)
            }
        }
    )"""
content = content.replace("    var isEditing by remember { mutableStateOf(false) }", launcher)

# Replace icon with AsyncImage
orig_icon = """            Icon(
                Icons.Default.Person,
                contentDescription = null,
                modifier = Modifier.size(100.dp),
                tint = MaterialTheme.colorScheme.primary
            )"""

new_icon = """            if (user.profileImageUrl.isNotEmpty()) {
                AsyncImage(
                    model = user.profileImageUrl,
                    contentDescription = "Profile Picture",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(120.dp)
                        .clip(CircleShape)
                        .clickable {
                            photoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                        }
                )
            } else {
                Surface(
                    modifier = Modifier
                        .size(120.dp)
                        .clip(CircleShape)
                        .clickable {
                            photoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                        },
                    color = MaterialTheme.colorScheme.primaryContainer
                ) {
                    Icon(
                        Icons.Default.Person,
                        contentDescription = "Upload Profile Picture",
                        modifier = Modifier
                            .padding(24.dp)
                            .fillMaxSize(),
                        tint = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }
            Text("Tap to change picture", style = MaterialTheme.typography.labelSmall, modifier = Modifier.padding(top = 8.dp))"""
content = content.replace(orig_icon, new_icon)

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)

