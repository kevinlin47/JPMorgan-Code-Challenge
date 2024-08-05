import requests

base_url = 'http://a41760c73978b4953a80c452f02c63b1-1582392590.us-east-1.elb.amazonaws.com'

tests_passed = 0
tests_failed = 0
total_tests = 0

def health_check():
    endpoint = '/healthcheck'
    url = base_url + endpoint
    response = requests.get(url)

    print(response)
    if (response.status_code != 200):
        print('Health Check Failed\n')
        global tests_failed
        tests_failed += 1
    else:
        print('Health Check Passed\n')
        global tests_passed
        tests_passed += 1
    global total_tests
    total_tests += 1

def readiness_check():
    endpoint = '/readiness'
    url = base_url + endpoint
    response = requests.get(url)

    print(response)
    if (response.status_code != 200):
        print('Readiness Check Failed\n')
        global tests_failed
        tests_failed += 1
    else:
        print('Readiness Check Passed\n')
        global tests_passed
        tests_passed += 1
        global total_tests
    total_tests += 1

def get_movie_by_title_check(test_case):
    endpoint = ''
    payload = {}
    global tests_passed
    global tests_failed
    global total_tests

    if test_case == 'invalid_parameter':
        endpoint = '/movies/title/'
        url = base_url + endpoint
        response = requests.get(url)

        print(response)
        if (response.status_code != 422):
            print('Invalid query parameter check - Failed\n')
            tests_failed += 1
        else:
            print('Invalid query parameter check - Passed\n')
            tests_passed += 1
    
    elif test_case =='missing_movie':
        endpoint = '/movies/title/'
        url = base_url + endpoint
        payload = {'movie_name': 'moviethatdoesnotexist'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 404):
            print('Missing movie check - Failed\n')
            tests_failed += 1
        else:
            print('Missing movie check - Passed\n')
            tests_passed += 1
    
    elif test_case == 'get_movie':
        endpoint = '/movies/title/'
        url = base_url + endpoint
        payload = {'movie_name': 'Black Hawk Down'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 200):
            print('Get movie check - Failed\n')
            tests_failed += 1
        else:
            print('Get movie check - Passed\n')
            tests_passed += 1
    
    else:
        print('Invalid test case for function get_movie_by_title_check\n')
        tests_failed += 1
    
    total_tests += 1

def get_movie_by_year_check(test_case):
    endpoint = ''
    payload = {}
    global tests_passed
    global tests_failed
    global total_tests

    if (test_case == 'no_query_parameter_check'):
        endpoint = '/movies/year/'
        url = base_url + endpoint
        response = requests.get(url)

        print(response)
        if (response.status_code != 422):
            print('No query parameter check - Failed\n')
            tests_failed += 1
        else:
            print('No query parameter check - Passed\n')
            tests_passed += 1
    elif (test_case == 'invalid_query_parameter_check'):
        endpoint = '/movies/year/'
        url = base_url + endpoint
        response = requests.get(url)

        print(response)
        if (response.status_code != 422):
            print('Invalid query parameter check - Failed\n')
            tests_failed += 1
        else:
            print('Invalid query parameter check - Passed\n')
            tests_passed += 1
    elif (test_case == 'missing_movies_for_year'):
        endpoint = '/movies/year/'
        url = base_url + endpoint
        payload = {'year': '1899'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 404):
            print('No movies found by year check - Failed\n')
            tests_failed += 1
        else:
            print('No movies found by year check - Passed\n')
            tests_passed += 1
    elif(test_case == 'get_movies_by_year'):
        endpoint = '/movies/year/'
        url = base_url + endpoint
        payload = {'year': '1995'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 200):
            print('Movies found by year check - Failed\n')
            tests_failed += 1
        else:
            print('Movies found by year check - Passed\n')
            tests_passed += 1
    else:
        print("Invalid test case for function get_movie_by_year_check\n")
    total_tests += 1
    

def get_movie_by_cast_check(test_case):
    endpoint = '/movies/cast/'
    url = base_url + endpoint
    payload = {}
    global tests_passed
    global tests_failed
    global total_tests

    if test_case == 'invalid_parameter':
        response = requests.get(url)

        print(response)
        if (response.status_code != 422):
            print('Invalid query parameter check - Failed\n')
            tests_failed += 1
        else:
            print('Invalid query parameter check - Passed\n')
            tests_passed += 1
    
    elif test_case =='missing_movie':
        payload = {'cast_member': 'somerandomperson'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 404):
            print('Missing movie check - Failed\n')
            tests_failed += 1
        else:
            print('Missing movie check - Passed\n')
            tests_passed += 1
    
    elif test_case == 'get_movie':
        payload = {'cast_member': 'Tom Hardy'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 200):
            print('Get movie check - Failed\n')
            tests_failed += 1
        else:
            print('Get movie check - Passed\n')
            tests_passed += 1
    
    else:
        print('Invalid test case for function get_movie_by_cast_check\n')
        tests_failed += 1
    
    total_tests += 1

def get_movie_by_genre_check(test_case):
    endpoint = '/movies/genre/'
    url = base_url + endpoint
    payload = {}
    global tests_passed
    global tests_failed
    global total_tests

    if test_case == 'invalid_parameter':
        response = requests.get(url)

        print(response)
        if (response.status_code != 422):
            print('Invalid query parameter check - Failed\n')
            tests_failed += 1
        else:
            print('Invalid query parameter check - Passed\n')
            tests_passed += 1
    
    elif test_case =='missing_movie':
        payload = {'genre': 'software'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 404):
            print('Missing movie check - Failed\n')
            tests_failed += 1
        else:
            print('Missing movie check - Passed\n')
            tests_passed += 1
    
    elif test_case == 'get_movie':
        payload = {'genre': 'Action'}
        response = requests.get(url, params=payload)

        print('request url = ' + response.url)
        print(response)
        if (response.status_code != 200):
            print('Get movie check - Failed\n')
            tests_failed += 1
        else:
            print('Get movie check - Passed\n')
            tests_passed += 1
    
    else:
        print('Invalid test case for function get_movie_by_genre_check\n')
        tests_failed += 1
    
    total_tests += 1

def main():

    print('Performing health check')
    health_check()

    print('Performing readiness check')
    readiness_check()

    print('Performing invalid query parameter for get movie by title')
    get_movie_by_title_check(test_case='invalid_parameter')
    print('Performing missing movie check for get movie by title')
    get_movie_by_title_check(test_case='missing_movie')
    print('Performing get movie check for get movie by title')
    get_movie_by_title_check(test_case='get_movie')

    print('Performing no query parameter check for get movie by year')
    get_movie_by_year_check(test_case='no_query_parameter_check')
    print('Performing invalid query parameter check for get movie by year')
    get_movie_by_year_check(test_case='invalid_query_parameter_check')
    print('Performing missing movies for get movie by year')
    get_movie_by_year_check(test_case='missing_movies_for_year')
    print('Performing get movies check for get movies by year')
    get_movie_by_year_check(test_case='get_movies_by_year')

    print('Performing invalid query parameter for get movie by cast')
    get_movie_by_cast_check(test_case='invalid_parameter')
    print('Performing missing movie check for get movie by cast')
    get_movie_by_cast_check(test_case='missing_movie')
    print('Performing get movie check for get movie by cast')
    get_movie_by_cast_check(test_case='get_movie')

    print('Performing invalid query parameter for get movie by genre')
    get_movie_by_genre_check(test_case='invalid_parameter')
    print('Performing missing movie check for get movie by genre')
    get_movie_by_genre_check(test_case='missing_movie')
    print('Performing get movie check for get movie by genre')
    get_movie_by_genre_check(test_case='get_movie')



    print('------------Test Summary------------\n')
    print("Tests Passed: " + str(tests_passed) + "/" + str(total_tests) + "\n")
    print("Tests Failed: " + str(tests_failed) + "/" + str(total_tests) + "\n")
if __name__ =="__main__":
    main()