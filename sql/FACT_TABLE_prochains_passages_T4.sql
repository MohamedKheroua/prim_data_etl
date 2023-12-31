-- Create prochains_passages_T4 table
CREATE TABLE prochains_passages_T4
(
	ResponseMessageIdentifier VARCHAR(100),
	ResponseTimestamp TIMESTAMP,
	Version NUMERIC,
	Status VARCHAR(20),
	RecordedAtTime TIMESTAMP,
	VehicleMode TEXT,
    PublishedLineName TEXT,
	DirectionName TEXT,
	OriginName TEXT,
	DestinationName TEXT,
	JourneyNote TEXT,
	FirstOrLastJourney TEXT,
	VehicleJourneyName TEXT,
	LineRef TEXT,
	DatedVehicleJourneyRef TEXT,
	DestinationRef TEXT,
	OperatorRef TEXT,
	DirectionRef TEXT,
	RouteRef TEXT,
	OriginRef TEXT,
	id_ExpectedDepartureTime_date INT,
	id_ExpectedDepartureTime_time INT,
	DestinationDisplay TEXT,
	DepartureStatus TEXT,
	id_ExpectedArrivalTime_date INT,
	id_ExpectedArrivalTime_time INT,
	id_AimedArrivalTime_date INT,
	id_AimedArrivalTime_time INT,
	ArrivalStatus TEXT,
	id_AimedDepartureTime_date INT,
	id_AimedDepartureTime_time INT,
	StopPointRef TEXT,
	ArrivalPlatformName TEXT,
	ArrivalProximityText TEXT,
    PRIMARY KEY (DatedVehicleJourneyRef,StopPointRef)
);