# ======================================
# GA implementation for school schedule creation
# ======================================

import numpy as np
from random import shuffle

# Five days in a week, from 8AM to 3PM
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

# Random schedule generator based on available subjects and slots
def generator(subjects : dict):
    subject_list = []
    for subject_name,subject_slots in subjects.items():
        subject_list += [subject_name] * subject_slots

    #Filling remaining slots with free time
    subject_list += [None] * (DAYS*HOURS - len(subject_list))

    #Randomization
    shuffle(subject_list)

    #Matrix configuration
    schedule = np.ndarray((DAYS,HOURS), dtype = object)
    schedule[:] = None
    for day in range(DAYS):
        for hour in range(HOURS):
            schedule[day][hour] = subject_list[day*DAYS+hour]

    return schedule


