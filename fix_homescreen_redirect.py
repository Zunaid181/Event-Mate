import re

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "r") as f:
    text = f.read()

orig_home = """fun HomeScreen(
    viewModel: AppViewModel,
    currentUser: User?,
    onSupplierClick: (String) -> Unit,
    onNavigateToPlanning: () -> Unit,
    onNavigateToVendor: () -> Unit,
    onNavigateToProfile: () -> Unit
) {"""

new_home = """fun HomeScreen(
    viewModel: AppViewModel,
    currentUser: User?,
    onSupplierClick: (String) -> Unit,
    onNavigateToPlanning: () -> Unit,
    onNavigateToVendor: () -> Unit,
    onNavigateToProfile: () -> Unit
) {
    LaunchedEffect(currentUser?.role) {
        if (currentUser != null && currentUser.role != "Planner") {
            onNavigateToVendor()
        }
    }"""

text = text.replace(orig_home, new_home)

with open("app/src/main/java/com/eventmate/ui/screens/HomeScreen.kt", "w") as f:
    f.write(text)
