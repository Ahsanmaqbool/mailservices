# Mail Service DRF API

This project is a mail service API developed using Django and Django REST Framework (DRF). It handles the scheduling and optimization of parcel deliveries using trains.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running the server, ensure you have the following installed:
- Python (3.8 or higher)
- Django (3.2 or higher)
- Django REST Framework
- PuLP (for linear programming optimization)

### Installing

To set up the project, follow these steps:

1. Clone the repository:
git clone [repository URL]


2. Navigate to the project directory:
cd [project directory]


3. Install the required packages:
pip install -r requirements.txt


4. Run migrations to set up the database:
python manage.py makemigrations
python manage.py migrate


### Running the Server

To start the Django development server, run:
python manage.py runserver


The server will start on `http://localhost:8000/`.

## Testing the Endpoints

You can test the endpoints using tools like Postman or cURL. Here are some examples of how to test the endpoints:

1. **Creating a Line:**
POST /api/lines/
{
    "name": "Line1",
    "status": "Available"
}

2. **Creating a Parcel:**
POST /api/parcels/
{
"weight": 10.5,
"volume": 100.0,
"status": "Pending",
"owner": 1
}

3. **Processing Shipments:**
POST /api/process-shipments/


Use similar POST requests for creating trains and bookings.

## Handling Ambiguities

Several key ambiguities in the project requirements were addressed as follows:

1. **Dynamic Train Capacity:** Train capacity is treated as dynamic, and the system updates the remaining capacity as parcels are assigned.

2. **Parcel Priority:** Parcels are prioritized on a first-come-first-serve basis.

3. **Train Re-submission:** Trains are immediately available for re-submission after a trip, post a simulated maintenance delay.

4. **Line Scheduling:** A scheduling system was implemented to manage train departures and avoid conflicts.

5. **Cost Calculation:** Shipping costs are calculated based on the parcel's proportion of the train's total weight and volume.


These decisions were made to ensure a clear and efficient design for the mail service system.
