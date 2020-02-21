class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # What instance variables will be useful for storing on the Near Earth Object?
        self.name = kwargs.get('name', 'No name gotten')
        self.id = kwargs.get('id', None)
        self.diameter_min_km = float(kwargs.get(
            'estimated_diameter_min_kilometers', 0))
        self.is_potentially_hazardous_asteroid = kwargs.get(
            'is_potentially_hazardous_asteroid', False)
        self.orbits = []

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        # How do we connect orbits back to the Near Earth Object?
        self.orbits.append(orbit)

    def __repr__(self):
        """returns information about the object for debugging purposes"""

        return f'NearEarthObject id:{self.id} name:{self.name} orbit_dates:{[orbit.close_approach_date for orbit in self.orbits]} harzardous_asteriod:{self.is_potentially_hazardous_asteroid}'

    def __str__(self):
        """Prints information about the object"""

        return f'NearEarthObject id:{self.id} name:{self.name} orbit_dates:{[orbit.close_approach_date for orbit in self.orbits]} harzardous_asteriod:{self.is_potentially_hazardous_asteroid}'


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.neo_name = kwargs.get('name', 'No name gotten')
        self.close_approach_date = kwargs.get('close_approach_date', None)
        self.miss_distance_kilometers = float(
            kwargs.get('miss_distance_kilometers', 0))

    def __str__(self):
        """returns information about the object"""

        return f'OrbitPath neo_name:{self.neo_name} close_approach_date:{self.close_approach_date} missed_distance_kilometers:{self.miss_distance_kilometers}'
