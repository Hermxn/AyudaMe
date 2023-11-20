AREA_CHOICES = (
    ("Animals", "Animals"),
    ("Appliances", "Appliances"),
    ("Children", "Children"),
    ("Cleaning", "Cleaning"),
    ("Computers", "Computers"),
    ("Construction", "Construction"),
    ("Education", "Education"),
    ("Home repair", "Home repair"),
    ("Other", "Other"),
    ("Sports", "Sports"),
    ("Transportation", "Transportation"),
)

STATUSES = (
    ("Pending", "Pending"),
    ("In progress", "In progress"),
    ("Done", "Done"),
    ("Declined", "Declined"),
    ("Under approval", "Under approval"),
)


class Statuses:
    PENDING = STATUSES[0][0]
    IN_PROGRESS = STATUSES[1][0]
    DONE = STATUSES[2][0]
    DECLINED = STATUSES[3][0]
    UNDER_APPROVAL = STATUSES[4][0]
