from collections import namedtuple, defaultdict
from enum import Enum
from operator import eq, ge, gt

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple(
        'Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?
        self.date = kwargs.get('date', None)
        self.end_date = kwargs.get('end_date', None)
        self.start_date = kwargs.get('start_date', None)
        self.filter = kwargs.get('filter', None)
        self.number = kwargs.get('number', None)
        self.return_object = kwargs.get('return_object', None)

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        date_search = Query.DateSearch(DateSearch.equals.name, self.date) if self.date else Query.DateSearch(DateSearch.between.name, [self.start_date, self.end_date])

        return_object = Query.ReturnObjects.get(self.return_object)

        filters = []

        return Query.Selectors(date_search, self.number, filters, return_object)


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        'is_hazardous': 'is_potentially_hazardous_asteroid',
        'diameter': 'diameter_min_km',
        'distance': 'miss_distance_kilometers'
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
        '=': eq,
        '>': gt,
        '>=': ge
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        return_value = defaultdict(list)

        for filter_option in filter_options:
            a_filter = filter_option.split(':')[0]
            if hasattr(NearEarthObject(), Filter.Options.get(a_filter)):
                return_value['NearEarthObject'].append(filter_option)
            elif hasattr(OrbitPath(), Filter.Options.get(a_filter)):
                return_value['OrbitPath'].append(filter_option)

        return return_value

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the 
        filtered_list = []
        for neo in results:
            operation = Filter.Operators.get(self.operation)
            field = Filter.Options.get(self.field)
            val = getattr(neo, field)
            try:
                if operation(val, self.value):
                    filtered_list.append(neo)
            except Exception as exp:
                if operation(str(val), str(self.value)):
                    filtered_list.append(neo)

        return filtered_list


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?
        self.date_search_type = None
        self.date_to_neos = db.get_date_to_neos_map()

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
        self.date_search_type = query.date_search.type
        date = query.date_search.values
        list_of_neos = []
        if self.date_search_type == DateSearch.equals.name:
            list_of_neos = self.apply_dateseaerch_equal(
                self.date_to_neos, date)
        elif self.date_search_type == DateSearch.between.name:
            list_of_neos = self.apply_datesearch_between(
                self.date_to_neos, date[0], date[1])
        filtered_neos = []
        for neo in list_of_neos:
            if neo.is_potentially_hazardous_asteroid:
                filtered_neos.append(neo)

        return filtered_neos[: query.number]

    def apply_dateseaerch_equal(self, a_neo_map, date):
        """ This function perfoms the date filtering when only one date and return the results

        :param a_neo_map: dict of date to neos mappings
                date: string date to filter for
        :return: A list of filtered neos
        """
        result = []
        for k, v in a_neo_map.items():
            if k == date:
                result += v
        return result

    def apply_datesearch_between(self, a_neo_map, start_date, end_date):
        """ This functions performs the date filtering when more than one date is specified and returns the result

        :param a_neo_map: dict of date to neos mappings
                start_date: string start date for filtering
                end_date: string end date for filtering
        :return: A list of filtered neos"""
        result = []
        for k, v in a_neo_map.items():
            if k >= start_date and k <= end_date:
                result += v
        return result
