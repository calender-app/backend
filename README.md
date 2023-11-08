# Calendar Event Backend App

This is a backend application built using Python 3.10, PostgreSQL, SQLAlchemy, FastAPI, and Swagger for managing calendar events.

## Prerequisites

Before you get started, make sure you have the following components installed on your system:

- Python 3.10
- PostgreSQL
- Docker (for running the app in containers)

## Setup

1. **Database Setup**

   - Make sure PostgreSQL is installed on your system.
   - Create a new database in PostgreSQL:

     ```sql
     CREATE DATABASE your_database_name;
     ```

     Replace `your_database_name` with the desired name for your database.

2. **Configuration**

   - Copy the `.env.example` file to a new file named `.env`.
   - Update the database-related variables in the `.env` file:

     ```dotenv
     DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database_name
     ```

     Replace the placeholders (`your_username`, `your_password`, and `your_database_name`) with your actual PostgreSQL username, password, and database name.

3. **Install Dependencies**

   Install the project dependencies by running the following command:

   ```shell
   pip install -r requirements.txt

4. **Run Migrations**
   
    Apply the database schema to your newly created database:
    
    ```shell
    alembic upgrade head

    This command will apply all the necessary migrations to create the tables and schema for your database.

5. **Start the Project**
   
   You can start the project using Docker or manually:

    - Using Docker:
  
        Build the Docker containers with the following commands:
        ```shell
        docker-compose build --no-cache
        docker-compose up

    - Manually:
  
        Start the FastAPI server with the following command:

        ```shell
        uvicorn app.main:app --host 0.0.0.0 --port {PORT_NUMBER} --reload
    
    Replace {PORT_NUMBER} with the desired port for the FastAPI server.

6. **Access the API**
    Once the application is running, you can access the API documentation and test the endpoints using Swagger. Open a web browser and navigate to: `http://localhost:{PORT_NUMBER}/docs`


# System Design

## Table Schema

Here's the schema for the `events` table in the database:

| Column             | Data Type | Description                                      |
|--------------------|-----------|--------------------------------------------------|
| event_id           | Integer   | Primary key for the event                       |
| title              | String    | Title of the event                              |
| description        | String    | Event description                                |
| start              | DateTime  | Start date and time of the event                |
| end                | DateTime  | End date and time of the event                  |
| note               | String    | Event notes                                      |
| repeat             | String    | Repeat pattern for recurring events              |
| is_full_day        | Boolean   | Flag indicating if the event is full-day        |
| repeat_interval    | Integer   | Interval for recurring events                   |
| color              | String    | Color code for the event                        |
| is_repeated_child  | Boolean   | Flag for identifying repeated child events      |

## Generating Recurring Events

1. Initialize an empty list called recurring_events to store the generated recurring events.

2. Generate a random color for the events using the get_random_color() function.

3. Start a loop that iterates from 1 to the specified recurring limit (appConstants.RECURRING_LIMITS[event_create.repeat]).

4. Inside the loop, clone the start and end times from the original event to create new start and end times for the recurring event.
5. Depending on the chosen repeat pattern (daily, weekly, or monthly), adjust the new start and end times based on the repeat interval.
6. Create a new recurring event by cloning the event_create object.
7. Set the start and end times of the recurring event to the adjusted values.
8. Mark the event as a repeated child by setting the is_repeated_child attribute to True.
9. Assign the random color to the recurring event.
10. Add the recurring event to the recurring_events list.
11. After the loop is completed, add all the generated recurring events to the database by bulk create

## Get events 

1. Take selected date from client(frontend), get the month of selected
2. Return only that month's event by /events API
3. If no selected provided set now as selected date
    - Filtering: 
      - /events support filtering, to filter events need to provide filter_string from client
      - Filtering will be applied to `title`, `description` and `note`
    - Pagination:
      - /events support paging, need to provide `skip` and `limit` from client