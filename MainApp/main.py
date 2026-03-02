# ======================================
# Implementing a GA to create a schedule
# ======================================

import numpy as np
from random import shuffle

#Five days in a week, from 8AM to 3PM
DAYS = 5
HOURS = 7

#Subjects as name: slots/week
subjects = {
    "math" : 4,
    "programming" : 4,
    "romanian": 3,
    "physics" : 3,
    "biology" : 2,
    "chemistry" : 2,
    "german": 2,
    "geography": 1,
    "sports" : 1,
    "history" : 1,
    "religion" : 1,
    "arts" : 1
}

