import re

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "r") as f:
    text = f.read()

orig_vendor_discover = """                NavigationBarItem(
                    icon = { Icon(Icons.Default.Search, contentDescription = "Discover") },
                    label = { Text("Discover") },
                    selected = false,
                    onClick = onNavigateToHome
                )"""
text = text.replace(orig_vendor_discover, "")

with open("app/src/main/java/com/eventmate/ui/screens/VendorDashboardScreen.kt", "w") as f:
    f.write(text)

with open("app/src/main/java/com/eventmate/ui/screens/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

orig_admin_discover = """                NavigationBarItem(
                    icon = { Icon(Icons.Default.Search, contentDescription = "Discover") },
                    label = { Text("Discover") },
                    selected = false,
                    onClick = onNavigateToHome
                )"""
text = text.replace(orig_admin_discover, "")

with open("app/src/main/java/com/eventmate/ui/screens/AdminDashboardScreen.kt", "w") as f:
    f.write(text)

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "r") as f:
    text = f.read()

orig_profile_discover = """                NavigationBarItem(
                    icon = { Icon(Icons.Default.Search, contentDescription = "Discover") },
                    label = { Text("Discover") },
                    selected = false,
                    onClick = onNavigateToHome
                )"""
new_profile_discover = """                if (user.role == "Planner") {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Search, contentDescription = "Discover") },
                        label = { Text("Discover") },
                        selected = false,
                        onClick = onNavigateToHome
                    )
                }"""
text = text.replace(orig_profile_discover, new_profile_discover)

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(text)
