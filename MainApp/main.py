# ======================================
# GA implementation for school schedule creation
# ======================================

import numpy as np
from random import shuffle
from random import randint

# Five days in a week, from 8AM to 3PM
DAYS = 5
HOURS = 7

#Subjects as name: slots/week
SUBJECTS = {
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

    # Filling remaining slots with free time
    subject_list += [None] * (DAYS*HOURS - len(subject_list))

    # Randomization
    shuffle(subject_list)

    # Matrix configuration
    schedule = np.ndarray((DAYS,HOURS), dtype = object)
    schedule[:] = None
    for day in range(DAYS):
        for hour in range(HOURS):
            schedule[day][hour] = subject_list[day*HOURS+hour]

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

        s = s[:-free_slots_count]         # this should remove all free slots for the day
        if s.count(None) > 0:            # if it doesn't, then we penalize
            fitness -= penalty_wrong_free_slots_placement
        # ============================================================================

        # ================== Other penalties =========================
        # to be added
        # ============================================================

    return fitness

# How many specimens we keep after selection
keep_percent = 0.2

# Selection process, top x% of all schedules given
def selection (list_of_potential_schedules : list):
    best_specimens = []

    # Ranking each potential schedule using our fitness function
    for schedule in list_of_potential_schedules:
        best_specimens += [(schedule,fitness(schedule))]

    # Ordering our schedules based on their fitness
    best_specimens.sort(key = lambda specimen: specimen[1], reverse = True)

    # Keeping the best x%
    best_specimens = best_specimens[:int(len(best_specimens)*keep_percent)]

    return best_specimens

# Create a new children schedule based on two parent schedules
def crossover (schedule1 : np.ndarray, schedule2: np.ndarray):

    # How many subjects we keep from parent1
    crossing_point = 0.5

    # Empty schedule
    child_schedule = np.ndarray((DAYS,HOURS), dtype = object)
    child_schedule[:] = None

    # We keep part of the subjects from parent1 intact, and fill the remaining slots from parent2's remaining subjects
    it_subjects = list(SUBJECTS.items())
    kept_subjects = dict(it_subjects[:int(len(SUBJECTS) * crossing_point)])
    unkept_subjects = dict(it_subjects[int(len(SUBJECTS) * crossing_point):])

    kept_subjects[None] = DAYS*HOURS - sum([v for k,v in SUBJECTS.items()])                  # add the free slots from parent1

    return child_schedule

# Using crossover randomly over our best schedules, we create our new generation
def new_generation(best_schedules : list):

    # We will store our new schedules as 'parent1_id - parent2_id' : child_schedule
    new_schedules = dict()

    # Getting back to our initial population count
    while(len(new_schedules) < int(1.0/keep_percent) * len(best_schedules)):
        # Pick 2 random parents
        parent1_id = randint(0,len(best_schedules)-1)
        parent2_id = randint(0,len(best_schedules)-1)

        # Don't apply crossover over the same parent
        if parent1_id == parent2_id:
            continue

        # Give each child an unique name
        child_name = f"{parent1_id}-{parent2_id}"

        # Add our new child to the list
        if child_name not in new_schedules.keys():
            new_schedules[child_name] = crossover(best_schedules[parent1_id][0], best_schedules[parent2_id][0])

    # Return a list of all created children
    return [child_schedule for child_name,child_schedule in new_schedules.items()]



# =================== Testing =======================
initial_schedules = [generator(SUBJECTS) for i in range(60)]
best_schedules = selection(initial_schedules)
new_schedules = new_generation(best_schedules)
print("Done!")




