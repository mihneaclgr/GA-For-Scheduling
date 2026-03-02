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

# Grading system for a particular schedule, used to determine the
# best potential schedules for the next generation
def fitness(schedule : np.ndarray):

    # Starting fitness score, decrementing for each penalty
    fitness = 1000

    # Penalty points
    penalty_days_has_too_many_free_slots = 20
    penalty_wrong_free_slots_placement=150

    #Iterating over each day to apply penalties
    for day in range(DAYS):
        subject_list_for_the_day = list(schedule[day,:])
        free_slots_count = subject_list_for_the_day.count(None)


        # ================== Penalties regarding free slots =========================
        # Penalty for days having too many free slots
        if (free_slots_count > 2):
            fitness -= penalty_days_has_too_many_free_slots

        # Penalty for days having a free slot that's not at the end of the day
        s = subject_list_for_the_day.copy()

        s = s[:free_slots_count]         # this should remove all free slots for the day
        if s.count(None) > 0:            # if it doesn't, then we penalize
            fitness -= penalty_wrong_free_slots_placement
        # ============================================================================

    return fitness


