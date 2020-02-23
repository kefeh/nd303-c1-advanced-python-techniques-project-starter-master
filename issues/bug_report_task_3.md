# Task 3 Bugs, Errors and Fixes

## issue 1: 
After running the tests, some tests failed. Below are the tests and their fixes

- ERROR: test_find_unique_number_between_dates_with_diameter (tests.test_neo_database.TestNEOSearchUseCases)
AttributeError: 'NearEarthObject' object has no attribute 'diameter_min_km'

## solution
Rename attribute in NearEarthObject model to `diameter_min_km`


## issue 2: 
- ERROR: test_find_unique_number_between_dates_with_diameter_and_hazardous_and_distance (tests.test_neo_database.TestNEOSearchUseCases)

AttributeError: 'OrbitPath' object has no attribute 'neo_name'

## solution
Rename an attribute `name` in OrbitPath to `neo_name`
