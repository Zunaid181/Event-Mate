import re

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "r") as f:
    text = f.read()

orig_auth_block = """                    if (role != "Planner" && role != "Admin") {
                        val supplierRef = db.collection("suppliers").document(uid)
                        val supplierMap = Supplier(
                            id = uid,
                            name = name + " Services",
                            category = role,
                            basePrice = 500,
                            rating = 5.0,
                            reviewCount = 0,
                            imageUrl = "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&q=80&w=800",
                            description = "Welcome to my new $role business on Event Mate! Please contact me for details.",
                            services = listOf(SupplierService("Basic Package", 500), SupplierService("Premium Package", 1000)),
                            location = "Sydney, NSW",
                            capacity = 150,
                            bookedDates = emptyList(),
                            maxCapacity = 150
                        )
                        batch.set(supplierRef, supplierMap)
                    }"""
text = text.replace(orig_auth_block, "")

with open("app/src/main/java/com/eventmate/ui/viewmodels/AppViewModel.kt", "w") as f:
    f.write(text)
