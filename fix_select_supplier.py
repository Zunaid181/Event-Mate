import re

with open("app/src/main/java/com/eventmate/ui/screens/SelectSupplierScreen.kt", "r") as f:
    text = f.read()

orig_filter = """        val capacityConflict = it.category.equals("Venue", true) && expectedGuests != null && it.maxCapacity != null && it.maxCapacity < expectedGuests!!
        isCategory && !dateConflict && !capacityConflict"""

new_filter = """        val capacityConflict = it.category.equals("Venue", true) && expectedGuests != null && it.maxCapacity != null && it.maxCapacity < expectedGuests!!
        isCategory && !dateConflict && !capacityConflict && it.isPublished"""

text = text.replace(orig_filter, new_filter)

with open("app/src/main/java/com/eventmate/ui/screens/SelectSupplierScreen.kt", "w") as f:
    f.write(text)
