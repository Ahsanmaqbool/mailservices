from datetime import datetime

import pulp
from django.utils import timezone

from .models import Train, Parcel, Line, Booking


def get_available_trains():
    current_time = timezone.now()
    return Train.objects.filter(status="Available", maintenance_check__lte=current_time)


def get_pending_parcels():
    return Parcel.objects.filter(status="Pending")


def process_optimization_results(assignment_vars):
    for parcel_id, train_id in assignment_vars:
        if pulp.value(assignment_vars[parcel_id, train_id]) == 1:
            # Retrieve the train and parcel objects
            train = Train.objects.get(id=train_id)
            parcel = Parcel.objects.get(id=parcel_id)

            # Choose an available line for the train
            line = choose_available_line(train)
            if line is None:
                continue  # Skip if no line is available

            # Update train and parcel statuses
            train.status = "Booked"
            train.current_weight += parcel.weight
            train.current_volume += parcel.volume
            train.save()

            parcel.status = "Shipped"
            parcel.save()

            # Create a booking record
            departure_time = timezone.now()
            Booking.objects.create(train=train, parcel=parcel, line=line, departure_time=departure_time)

            # Update line status to "Occupied" for 3 hours
            line.status = "Occupied"
            line.save()
            # Schedule to make the line available after 3 hours
            make_line_available_after(line, hours=3)


def choose_available_line(train):
    # This function chooses an available line for the train
    for line in train.lines.all():
        if line.status == "Available":
            return line
    return None


def make_line_available_after(line, hours=3):
    # Schedule a task to make the line available after n hours
    # This could be implemented with a background task scheduler like Celery
    pass


def assign_parcels_to_trains():
    available_trains = Train.objects.filter(status="Available")
    pending_parcels = Parcel.objects.filter(status="Pending")

    for train in available_trains:
        for parcel in pending_parcels:
            # Check if the parcel fits in the train
            if parcel_fits_train(parcel, train):
                # Create a booking
                Booking.objects.create(
                    train=train,
                    parcel=parcel,
                    line=choose_line_for_train(train),
                    departure_time=datetime.now()
                )
                # Update statuses
                train.status = "Booked"
                parcel.status = "Shipped"
                train.save()
                parcel.save()


def parcel_fits_train(parcel, train):
    # Check weight and volume constraints
    return parcel.weight <= train.max_weight and parcel.volume <= train.max_volume


def choose_line_for_train(train):
    # Implement logic to choose an available line
    # This is a placeholder function
    available_lines = Line.objects.filter(status="Available")
    return available_lines.first() if available_lines.exists() else None


def optimize_parcel_assignment():
    # Define the problem
    prob = pulp.LpProblem("ParcelAssignment", pulp.LpMinimize)

    trains = get_available_trains()
    parcels = get_pending_parcels()

    # Decision variables: whether a parcel i is assigned to a train j
    assignment_vars = pulp.LpVariable.dicts("assign",
                                            [(i.id, j.id) for i in parcels for j in trains],
                                            cat='Binary')

    # Objective function: Minimize the total cost of assignments
    prob += pulp.lpSum([assignment_vars[i.id, j.id] * j.cost for i in parcels for j in trains])

    # Constraints
    for j in trains:
        # Train capacity constraints
        prob += pulp.lpSum([assignment_vars[i.id, j.id] * i.weight for i in parcels]) <= j.max_weight
        prob += pulp.lpSum([assignment_vars[i.id, j.id] * i.volume for i in parcels]) <= j.max_volume

    for i in parcels:
        # Each parcel should be assigned to exactly one train
        prob += pulp.lpSum([assignment_vars[i.id, j.id] for j in trains]) == 1

    # Solve the problem
    prob.solve()

    process_optimization_results(assignment_vars)
