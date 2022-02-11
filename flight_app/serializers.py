"""DRF serializers:
    - flight serializer
    - weather serializer
    - search serializer
"""
from rest_framework import serializers

from flight_app.models import Flight, Aircraft, Airline, Status, Airport, FlightAirport, Weather
from django.conf import settings


class AirlineSerializer(serializers.ModelSerializer):
    """DRF serializer for Airline model"""
    airlineCode = serializers.IntegerField(source='code')
    prefixICAO = serializers.CharField(source='ICAO', allow_null=True)
    prefixIATA = serializers.CharField(source='IATA')

    class Meta:
        """Set all fields that should be serialized
        all fields has relation to model  Airline"""
        model = Airline
        fields = ['airlineCode', 'prefixICAO', 'prefixIATA']

    def create(self, validated_data):
        """Create new Airline in DB in case current airline does NOT exist in DB,
        return airline - obj of Airline"""
        obj, created = Airline.objects.get_or_create(
            code=validated_data['code'], IATA=validated_data['IATA'], defaults={'ICAO': validated_data['ICAO']}
        )
        return obj


class AircraftSerializer(serializers.ModelSerializer):
    """DRF serializer for Aircraft model"""
    aircraftRegistration = serializers.CharField(source='registration')
    aircraftType = serializers.DictField(child=serializers.CharField(), source='type')

    class Meta:
        """Set all fields that should be serialized
            all fields has relation to model  Aircraft"""
        model = Aircraft
        fields = ['aircraftRegistration', 'aircraftType']

    def validate_aircraftType(self, value):
        """ Take iataMain value from dict {aircraftType: {'iataMain': 'value', ...}
        :param value: value from aircraftType: DictField
        :return: iataMain: CharField
        """
        return value['iataMain']

    def create(self, validated_data):
        """Create new Aircraft in DB in case current aircraft does NOT exist in DB,
        return aircraft - obj of Aircraft"""
        obj, created = Aircraft.objects.get_or_create(
            registration=validated_data['registration'], type=validated_data['type']
        )
        return obj


class AirportSerializer(serializers.ListSerializer):
    """DRF List serializer for Airport model"""
    child = serializers.CharField()

    def save(self, **kwargs):
        """Create new Airport in DB in case current airport does NOT exist in DB,
            return airport - obj of Airport"""
        for item in self.validated_data:
            Airport.objects.get_or_create(name=item)


class FlightSerializer(serializers.ModelSerializer):
    """DRF serializer for Flight model"""
    flightName = serializers.CharField(source='name')
    lastUpdatedAt = serializers.DateTimeField(source='last_update')
    scheduleDateTime = serializers.DateTimeField(source='schedule_date_time')
    actualLandingTime = serializers.DateTimeField(source='actual_landing_time', allow_null=True)
    actualOffBlockTime = serializers.DateTimeField(source='actual_off_time', allow_null=True)
    expectedTimeBoarding = serializers.DateTimeField(source='expected_boarding_time', allow_null=True)
    estimatedLandingTime = serializers.DateTimeField(source='estimate_landing_time', allow_null=True)
    airlineCode = serializers.CharField(source='airline')
    aircraftRegistration = serializers.CharField(source='aircraft')
    flightDirection = serializers.CharField(max_length=1)
    publicFlightState = serializers.DictField(source='status')
    route = serializers.DictField(source='airport')

    class Meta:
        """Set all fields that should be serialized
            all fields has relation to model  Flight,
            exclude 'flightDirection' - it has no relate to model"""
        model = Flight
        fields = ['id', 'flightName', 'lastUpdatedAt', 'scheduleDateTime', 'actualLandingTime',
                  'actualOffBlockTime', 'expectedTimeBoarding', 'estimatedLandingTime',
                  'airlineCode', 'aircraftRegistration', 'flightDirection', 'publicFlightState', 'route']

    def validate_route(self, value):
        """Since we have base airport - Schiphol "AMS",
        it has been added into DB in ADVANCE.
        Take Airport instances from DB Airport model
            :return instances of Airport"""
        destinations = Airport.objects.filter(name__in=value['destinations'])
        return destinations

    def validate_publicFlightState(self, value):
        """Since we have only several statuses,
        all of them have been added into DB in ADVANCE.
        Take Status instances from DB Status model
            :return instances of Status"""
        statuses = Status.objects.filter(name__in=value['flightStates'])
        return statuses

    def validate_airlineCode(self, value):
        """Take Airline instances from DB Airline model
            :return instances of Airline"""
        check_airline = Airline.objects.filter(code=value).first()
        return check_airline

    def validate_aircraftRegistration(self, value):
        """Take Aircraft instances from DB Aircraft model
            :return instances of Aircraft"""
        check_aircraft = Aircraft.objects.filter(registration=value).first()
        return check_aircraft

    @staticmethod
    def insert_into_flight_airport(direction: str, flight: Flight, airports: list[Airport]) -> None:
        """Insert data into FlightAirport model.
        Determine the airport of departure and arrive
        Add transit airports (if it exists)
            :param direction: departure flight "D" or an arrival flight "A".
            :param flight: Flight model object
            :param airports Airport model objects"""
        # get base Amsterdam Schiphol airport (id=1, name="AMS") from settings.py
        base_airport = Airport.objects.get(name=settings.AMSTERDAM_BASE_AIRPORT_NAME)
        if direction == 'A':
            # Determine the airport of departure and arrive
            flight_airport = FlightAirport(flight=flight, airport=airports[0], from_to_marker='DEP')
            flight_airport_base = FlightAirport(flight=flight, airport=base_airport, from_to_marker='ARR')
        else:
            # Determine the airport of departure and arrive
            flight_airport = FlightAirport(flight=flight, airport=airports[0], from_to_marker='ARR')
            flight_airport_base = FlightAirport(flight=flight, airport=base_airport, from_to_marker='DEP')
        flight_airport.save()
        flight_airport_base.save()
        # add transition airports(if it exists)
        if len(airports) != 1:
            for airport in airports[1:]:
                flight_airport = FlightAirport(flight=flight, airport=airport, from_to_marker='TRAN')
                flight_airport.save()

    def save(self, **kwargs):
        """Check if current Flight instance not in DB (check by concurrency 'name' and 'schedule_date_time')
            - crete new one
            if current flight has different 'last_update' datetime
            - update flight's data in DB"""
        instance = Flight.objects.filter(
            name=self.validated_data['name'], schedule_date_time=self.validated_data['schedule_date_time']
        ).first()
        if not instance:
            return self.create(self.validated_data)
        if instance.last_update != self.validated_data['last_update']:
            return self.update(instance, self.validated_data)

    def create(self, validated_data):
        """Create new Flight in DB"""
        # pop statuses, airports, direction from all validated data
        statuses = validated_data.pop('status')
        airports = validated_data.pop('airport')
        direction = validated_data.pop('flightDirection')

        # crete flight object
        flight = Flight.objects.create(**validated_data)
        # add data in FlightStatus model
        flight.status.set(statuses)
        # add data in FlightAirport model (look insert_into_fligt_airport method above)
        self.insert_into_flight_airport(direction, flight, airports)
        # todo: logger
        return flight

    # .save() will update the existing flight instance.
    def update(self, instance, validated_data):
        """Update flight's data"""
        instance.name = validated_data.get('name', instance.name)
        instance.last_update = validated_data.get('last_update', instance.last_update)
        instance.actual_landing_time = validated_data.get('actual_landing_time', instance.actual_landing_time)
        instance.actual_off_time = validated_data.get('actual_off_time', instance.actual_off_time)
        instance.expected_boarding_time = validated_data.get('expected_boarding_time', instance.expected_boarding_time)
        instance.estimate_landing_time = validated_data.get('estimate_landing_time', instance.estimate_landing_time)
        instance.aircraft = validated_data.get('aircraft', instance.aircraft)

        # pop statuses from all validated data clear previous statuses and set new
        statuses = validated_data.pop('status')
        instance.status.clear()
        instance.status.set(statuses)
        instance.save()
        # todo: logger
        return instance


class ResponseFlightAirportSerializer(serializers.HyperlinkedModelSerializer):
    """DRF serializer for api response based on FlightAirport model
    Serializer output:
        - name: Airport.name field
        - from_to_marker: FlightAirport model field"""
    name = serializers.ReadOnlyField(source='airport.name')
    from_to_marker = serializers.ReadOnlyField()

    class Meta:
        """Set fields that should be serialized
            name: field has relation to model  Airport
            from_to_marker: field has relation to model FlightAirport"""
        model = FlightAirport
        fields = ['name', 'from_to_marker']


class ResponseFlightSerializer(serializers.ModelSerializer):
    """DRF serializer for api response based on Flight model
    Serializer output related tables data (Airport model, Airline model)
    Status and Airport related tables data contain only names(exclude id)
    """
    # redefine Status and Airport output
    status = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    airport = ResponseFlightAirportSerializer(source='flightairport_set', many=True)

    class Meta:
        """Set all fields that should be serialized
            all fields has relation to model  Flight
        Include all fields of related models"""
        model = Flight
        fields = '__all__'
        # Add fields of related models
        depth = 1


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        """Set all fields that should be serialized
            all fields has relation to model  Weather
        """
        model = Weather
        fields = '__all__'

    def create(self, validated_data):
        """Create new hourly_weather in DB in case current hour weather forecast does NOT exist in DB,
            else update hourly_weather forcast
        return weather forecast - obj of Weather"""
        obj, created = Weather.objects.update_or_create(
            datetime=validated_data['datetime'],
            defaults={'wind_cdir_full': validated_data['wind_cdir_full'],
                      'wind_spd': validated_data['wind_spd'],
                      'temp': validated_data['temp'],
                      'precip': validated_data['precip'],
                      'snow': validated_data['snow'],
                      'rh': validated_data['rh'],
                      'clouds': validated_data['clouds']}
        )
        return obj


class RequestSearchSerializer(serializers.Serializer):
    """DRF serializer for ES search request data
        const: SIZE: int, number cof returning docs per page
        const: PAGE: int, page number
        :param name: Option[str], search by full or part of word, ES field 'name'
        :param date: Option[date], filter by date, ES field 'schedule_date_time'
        :param start_date: Option[date], filter dy period of dates, ES field 'schedule_date_time'
        :param last_date: Option[date], filter dy period of dates, ES field 'schedule_date_time'
        :param code: Option[int], filter by airline code, ES field 'airline.code'
        :param ICAO: Option[str], filter by airline ICAO abbr, ES field 'airline.ICAO'
        :param ICAO: Option[str], filter by airline IATA abbr, ES field 'airline.IATA'
        :param status: Option[str], filter by status abbr, ES field 'status.name'
        :param airport: Option[str], filter by airport abbr, ES field 'airport.name'
        :param connected: Optional[choices= 'y' or 'n'],
                filter by connected or not flights, ES field 'airport.from_to_marker'
        :param pagination: int, by default=10, quantity returning docs
        """
    # pagination const
    SIZE = 10
    PAGE = 0

    name = serializers.CharField(max_length=15, allow_null=True)

    date = serializers.DateField(allow_null=True)
    start_date = serializers.DateField(allow_null=True)
    last_date = serializers.DateField(allow_null=True)

    code = serializers.IntegerField(allow_null=True)
    ICAO = serializers.CharField(max_length=3, allow_null=True)
    IATA = serializers.CharField(max_length=2, allow_null=True)

    status = serializers.CharField(max_length=3, allow_null=True)

    airport = serializers.CharField(max_length=3, allow_null=True)
    connected = serializers.ChoiceField(choices=('y', 'n'), allow_null=True)

    size = serializers.IntegerField(default=SIZE)
    page = serializers.IntegerField(default=PAGE)

    def validated_code(self, value):
        """Convert request's code param to int"""
        return self.validated_code_and_size(value)

    def validated_size(self, value):
        """Convert request's size param to int"""
        return self.validated_code_and_size(value)

    def validated_page(self, value):
        """Convert request's page param to int"""
        return self.validated_code_and_size(value)

    @staticmethod
    def validated_code_and_size(value):
        """Convert request's params to int
        Raise ValidationError in case can't convert to int"""
        try:
            int(value)
        except ValueError() as error:
            raise serializers.ValidationError(error)
        return value

    def validate(self, data):
        """ Check that both parameters(start and last dates) provided
        Check that the start date is before the last one
        Else raise ValidationError"""
        if (not data['start_date'] and data['last_date']) or (data['start_date'] and not data['last_date']):
            raise serializers.ValidationError("2 dates must be provided")
        if data['start_date'] and data['last_date']:
            if data['start_date'] > data['last_date']:
                raise serializers.ValidationError("finish must occur after start")
        return data
