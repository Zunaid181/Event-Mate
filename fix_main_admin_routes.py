import re

with open("app/src/main/java/com/eventmate/MainActivity.kt", "r") as f:
    text = f.read()

new_routes = """        composable("admin_dashboard") {
            AdminDashboardScreen(
                viewModel = viewModel,
                currentUser = currentUser,
                onNavigateToHome = { navController.navigate("home") { popUpTo("home") { inclusive = true } } },
                onNavigateToProfile = { navController.navigate("profile") { popUpTo("home") } },
                onSupplierClick = { supplierId -> navController.navigate("supplier/$supplierId?fromPlan=false") },
                onUserClick = { userId -> navController.navigate("admin_user/$userId") }
            )
        }
        composable(
            route = "admin_user/{userId}",
            arguments = listOf(navArgument("userId") { type = NavType.StringType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getString("userId") ?: return@composable
            AdminUserProfileScreen(
                viewModel = viewModel,
                userId = userId,
                onBackClick = { navController.popBackStack() }
            )
        }
    }
}
"""

text = text.replace("    }\n}", new_routes)

with open("app/src/main/java/com/eventmate/MainActivity.kt", "w") as f:
    f.write(text)
