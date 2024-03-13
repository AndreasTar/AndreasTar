'''
Inspired by GitHub user 'Andrew6rant's README.
Their profile link : https://github.com/Andrew6rant
Their README repo link : https://github.com/Andrew6rant
'''

import datetime
from xml.dom import minidom
from dateutil import relativedelta
import time

import os
import requests

LOG_FILE_PATH = "data/log.xml"
BIRTHDAY = datetime.datetime(2001, 3, 18)

#HEADERS = {'authorization': 'token '+ os.environ['ACCESS_TOKEN']}
HEADERS = {'authorization': 'token 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'}
#USER_NAME = os.environ['USER_NAME'] # 'AndreasTar'
USER_NAME = 'AndreasTar'

QUERY_COUNT = {
    'fetchUserData': 0,
    'fetchStars': 0,
    'fetchCommits': 0
}

def ageCalculator() -> str:
    """
    Returns the length of time since i was born
    e.g. 'XX years, XX months, XX days'
    """

    age = relativedelta.relativedelta(datetime.datetime.today(), BIRTHDAY)
    return "{} {}, {} {}, {} {}{}".format(
        age.years, "year" + ("s" if age.years != 1 else ""),
        age.months, "month" + ("s" if age.months != 1 else ""),
        age.days,  "day" + ("s" if age.days != 1 else ""),
        " 🎂" if (age.months == 0 and age.days == 0) else ""
    )

def makeRequest(funcName, query, vars):
    """
    Returns a request, or raises an Exception if the response does not succeed.
    """
    request = requests.post(
       'https://api.github.com/graphql',
       json = {
           'query': query,
           'variables': vars
       },
       headers = HEADERS
    )
    global QUERY_COUNT
    QUERY_COUNT[funcName] += 1
    #TODO status code 200 is also returned on rate limit error. handle it
    if request.status_code == 200:
        return request
    raise Exception(funcName, ' has failed with a', request.status_code, request.text, QUERY_COUNT)

def fetchCommits(startDate = None, endDate = None) -> int:
    """
    Uses GitHub's GraphQL v4 API to fetch the total commit count between 
    the input dates
    """

    query = """
    query($login: String!) {
        user(login: $login) {
            contributionsCollection {
                contributionCalendar {
                    totalContributions
                }
            }
        }
    }"""

    vars = {
        'start_date': startDate,
        'end_date': endDate,
        'login': USER_NAME
    }
    request = makeRequest(fetchCommits.__name__, query, vars)
    return int(request.json()['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions'])

def fetchStars(ownerAffil = ['OWNER', 'COLLABORATOR']) -> tuple[requests.Response, int]:
    query = """
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!) {
        user(login: $login) {
            repositories(first: 100, ownerAffiliations: $owner_affiliation) {
                totalCount
                nodes {
                    ... on Repository {
                        stargazerCount
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }"""

    vars = {
        'owner_affiliation': ownerAffil,
        'login': USER_NAME,
    }
    request = makeRequest(fetchStars.__name__, query, vars)
    if request.status_code == 200:
        return (
            request.json()['data']['user']['repositories']['totalCount'],
            _calculateStars(request.json()['data']['user']['repositories']['nodes'])
        )

def _calculateStars(inData) -> int:
    total = 0
    for node in inData:
        total += node['stargazerCount']
    return total

def fetchUserData(username):
    query = """
    query($login: String!){
        user(login: $login) {
            id
            createdAt
        }
    }"""
    vars = {'login': username}
    request = makeRequest(fetchUserData.__name__, query, vars)
    return {'id': request.json()['data']['user']['id']}, request.json()['data']['user']['createdAt']

def _performanceCounter(funct, *args):
    """
    Calculates the time it takes for a function to run
    Returns the function result and the time differential
    """
    start = time.perf_counter()
    funct_return = funct(*args)
    return funct_return, time.perf_counter() - start

def _formatData(query_type, difference, funct_return=False, whitespace=0):
    """
    Prints a formatted time differential
    Returns formatted result if whitespace is specified, otherwise returns raw result
    """
    print('{:<27}'.format('   ' + query_type + ':'), sep='', end='')
    print('{:>12}'.format('%.4f' % difference + ' s ')) if difference > 1 else print('{:>12}'.format('%.4f' % (difference * 1000) + ' ms'))
    if whitespace:
        return f"{'{:,}'.format(funct_return): <{whitespace}}"
    return funct_return

if __name__ == '__main__':

    userData, fetchUserTime = _performanceCounter(fetchUserData, USER_NAME)
    _formatData('account data', fetchUserTime)
    userID, userCreatedData = userData
    ageData, ageCalculatorTime = _performanceCounter(ageCalculator)
    _formatData('age data (internal)', ageCalculatorTime)
    #userCreatedData, datetime.datetime.now().replace(microsecond=0).isoformat()+'Z'
    commitData, fetchCommitsTime = _performanceCounter(fetchCommits)
    _formatData('commits data', fetchCommitsTime, commitData)
    starsData, fetchStarsTime = _performanceCounter(fetchStars)
    _formatData('stars data', fetchStarsTime, starsData)


