# Web_project_Tkachuk
    Temporary version README

Create API to display time of the take-off and landing  the aircraft with weather data at that time

  - Create API call to display all flights within the specified time interval
  - Create API call to display all information (including weather) for a specific flight
  - Create a task for downloading data from the API at 2 a.m. every day (that is, the select task 
  will be launched to download all the information we need about the weather and flights from the api 
  to the database)
  - Make versioning for API (like in the first version there will be information about flights and 
  weather, and in the second information about flights and weather and the ozone layer)

To deploy the project, you need  Docker и Compose and copy .env.dist file

    cp .env.dist .env

For start RUN command

    docker-compose up -d 

Project has custom django command for Flights service, run

    python manage.py run_parse_flights [date] [-p --period]

or for help run

    python manage.py run_parse_flights -h