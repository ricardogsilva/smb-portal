INSERT INTO tracks_collectedpoint (
    vehicle_type,
    track_id,
    the_geom,
    accelerationx,
    accelerationy,
    accelerationz,
    accuracy,
    batconsumptionperhour,
    batterylevel,
    devicebearing,
    devicepitch,
    deviceroll,
    elevation,
    gps_bearing,
    humidity,
    lumen,
    pressure,
    proximity,
    speed,
    temperature,
    sessionid,
    timestamp
) VALUES (
    %(vehicle_type)s,
    %(track_id)s,
    ST_SetSRID(ST_MakePoint(%(longitude)s, %(latitude)s), 4326),
    %(accelerationx)s,
    %(accelerationy)s,
    %(accelerationz)s,
    %(accuracy)s,
    %(batconsumptionperhour)s,
    %(batterylevel)s,
    %(devicebearing)s,
    %(devicepitch)s,
    %(deviceroll)s,
    %(elevation)s,
    %(gps_bearing)s,
    %(humidity)s,
    %(lumen)s,
    %(pressure)s,
    %(proximity)s,
    %(speed)s,
    %(temperature)s,
    %(sessionid)s,
    %(timestamp)s
)