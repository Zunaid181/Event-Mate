import re

with open("app/src/main/java/com/eventmate/MainActivity.kt", "r") as f:
    text = f.read()

orig_home = """                onNavigateToVendor = { navController.navigate("vendor") { popUpTo("home") } },"""
new_home = """                onNavigateToVendor = { 
                    if (currentUser?.role == "Admin") {
                        navController.navigate("admin_dashboard") { popUpTo("home") }
                    } else {
                        navController.navigate("vendor") { popUpTo("home") }
                    }
                },"""
text = text.replace(orig_home, new_home)

orig_plan = """                onNavigateToVendor = { navController.navigate("vendor") { popUpTo("home") } },"""
new_plan = """                onNavigateToVendor = { 
                    if (currentUser?.role == "Admin") {
                        navController.navigate("admin_dashboard") { popUpTo("home") }
                    } else {
                        navController.navigate("vendor") { popUpTo("home") }
                    }
                },"""
text = text.replace(orig_plan, new_plan) # this will probably fail if it replaces twice, wait, the file has it multiple times.

with open("app/src/main/java/com/eventmate/MainActivity.kt", "w") as f:
    f.write(text)
