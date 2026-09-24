import re

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "r") as f:
    text = f.read()

orig_nav = """                NavigationBarItem(
                    icon = { Icon(Icons.Default.Star, contentDescription = "Plan") },
                    label = { Text("Plan") },
                    selected = false,
                    onClick = onNavigateToPlanning
                )"""

new_nav = """                if (user.role == "Planner") {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Star, contentDescription = "Plan") },
                        label = { Text("Plan") },
                        selected = false,
                        onClick = onNavigateToPlanning
                    )
                }"""

text = text.replace(orig_nav, new_nav)

with open("app/src/main/java/com/eventmate/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(text)
