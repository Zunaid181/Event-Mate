import re

with open("app/src/main/java/com/eventmate/ui/screens/SupplierProfileScreen.kt", "r") as f:
    text = f.read()

orig_img = """            item {
                AsyncImage(
                    model = supplier.imageUrl,
                    contentDescription = supplier.name,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(250.dp)
                )
            }"""

new_img = """            item {
                if (supplier.imageUrls.isNotEmpty()) {
                    androidx.compose.foundation.lazy.LazyRow(modifier = Modifier.fillMaxWidth().height(250.dp)) {
                        items(supplier.imageUrls.size) { index ->
                            AsyncImage(
                                model = supplier.imageUrls[index],
                                contentDescription = supplier.name,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier
                                    .fillParentMaxWidth()
                                    .fillMaxHeight()
                            )
                        }
                    }
                } else {
                    AsyncImage(
                        model = supplier.imageUrl,
                        contentDescription = supplier.name,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(250.dp)
                    )
                }
            }"""
text = text.replace(orig_img, new_img)

with open("app/src/main/java/com/eventmate/ui/screens/SupplierProfileScreen.kt", "w") as f:
    f.write(text)
