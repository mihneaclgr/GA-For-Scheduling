# ======================================
# GA implementation for school schedule creation
# ======================================
from typing import Any

import numpy as np
from random import shuffle
from random import randint

from numpy import dtype, ndarray

# Five days in a week, from 8AM to 3PM
DAYS = 5
HOURS = 7

#Subjects as name: slots/week
SUBJECTS = {
    "math" : 4,
    "programming" : 7,
    "romanian": 3,
    "physics" : 3,
    "biology" : 2,
    "chemistry" : 2,
    "german": 2,
    "geography": 1,
    "sports" : 1,
    "history" : 1,
    "religion" : 1,
    "arts" : 1,
    "reasoning": 1
}

# Random schedule generator based on available subjects and slots
def generator(subjects : dict) -> np.ndarray:
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

# Grading system for a particular schedule
def fitness(schedule : np.ndarray) -> int:

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
def selection (list_of_potential_schedules : list) -> list[tuple]:
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
def crossover (schedule1 : np.ndarray, schedule2: np.ndarray) -> np.ndarray:
    # How many subjects we keep from parent1
    crossing_point = 0.5

    # Empty schedule
    child_schedule = np.ndarray((DAYS,HOURS), dtype = object)
    child_schedule[:] = ''

    # We keep part of the subjects from parent1 intact, and fill the remaining slots from parent2's remaining subjects
    it_subjects = list(SUBJECTS.items())
    kept_subjects = dict(it_subjects[:int(len(SUBJECTS) * crossing_point)])
    unkept_subjects = dict(it_subjects[int(len(SUBJECTS) * crossing_point):])

    kept_subjects[None] = DAYS*HOURS - sum([v for k,v in SUBJECTS.items()])          # add the free slots from parent1

    # Keep schedule1 part intact
    for day in range(DAYS):
        for hour in range(HOURS):
            if schedule1[day][hour] in kept_subjects.keys():
                child_schedule[day][hour] = schedule1[day][hour]

    # ================= List of all remaining slots that need to be placed =================
    # flatten schedule2
    schedule2_as_a_list = [subject
                           for subject_list_for_the_day in schedule2.tolist()
                           for subject in subject_list_for_the_day]
    # remove kept subjects from schedule1
    schedule2_as_a_list = [subject
                           for subject in schedule2_as_a_list
                           if subject not in kept_subjects.keys()]
    # reverse the list, to use pop() later
    schedule2_as_a_list.reverse()

    # place missing slots using schedule2
    for day in range(DAYS):
        for hour in range(HOURS):
            if child_schedule[day][hour] == '':
                child_schedule[day][hour] = schedule2_as_a_list.pop()
    return child_schedule

# Using crossover randomly over our best schedules, we create our new generation
def new_generation(best_schedules : list) -> list[np.ndarray]:

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

# Small mutation for generation improvement
def mutation(schedule: np.ndarray) -> np.ndarray:
    mutated_schedule: ndarray[tuple[Any, ...], dtype[Any]] = schedule.copy()

    # Pick 2 random subjects and switch them
    subject1 = randint(0,DAYS*HOURS-1)
    subject2 = randint(0,DAYS*HOURS-1)
    subject1 = (subject1//HOURS,subject1%HOURS)
    subject2 = (subject2//HOURS,subject2%HOURS)
    
    mutated_schedule[subject1[0]][subject1[1]], mutated_schedule[subject2[0]][subject2[1]] = mutated_schedule[subject2[0]][subject2[1]], mutated_schedule[subject1[0]][subject1[1]]

    return mutated_schedule




# =================== Testing =======================

# Initial population
initial_schedules = [generator(SUBJECTS) for i in range(60)]
generation = 0
new_schedule_fitness = 0
schedules = initial_schedules

elite_schedules = []

while new_schedule_fitness != 1000:
    generation += 1

    # Select the best specimens
    best_schedules = selection(schedules)

    # Crossover for new population
    new_schedules = new_generation(best_schedules)

    # Mutate each member of the new population
    new_schedules = [mutation(s) for s in new_schedules]

    # Keep the best children from the previous generation
    new_schedules.pop()
    new_schedules += [best_schedules[0][0]]

    # Evolution stop criteria
    for new_schedule in new_schedules:
        new_schedule_fitness = fitness(new_schedule)
        if new_schedule_fitness == 1000:
            # Keep all the good schedules
            elite_schedules += [(new_schedule,new_schedule_fitness)]

    # Re-iterate the loop
    schedules = new_schedules

elite_schedules.sort(key=lambda x: x[1], reverse=True)
found_schedule = elite_schedules[0]
print(generation)
# =====================================================================
