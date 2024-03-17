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

import svg
from textwrap import dedent


BIRTHDAY = datetime.datetime(2001, 3, 18)

#HEADERS = {'authorization': 'token '+ os.environ['ACCESS_TOKEN']}
#USER_NAME = os.environ['USER_NAME'] # 'AndreasTar'

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

def createSvgData():

    svgwidth = 970
    svgheight = 530

    dy = 20


    styles = svg.Style(
        text = dedent("""
                      .category { font: bold 30px; fill: FF9536 }
                      .data { fill: 8FE9FF }
                      .extras { fill: 999999 }
                      .titles { fill: FF5D79 }
                      """), 
    )

    # IDEA on top of the readme, a procedural ascii day-night cycle scene

    # #FF9536 main
    # #8FE9FF data
    # #999999 extra data
    # #FF5D79 titles

    # i want to have:

    # date of birth | done almost
    # where i live | done
    # degree / uni | done

    # languages | done
    # hobbies | done
    # interests | done
    # projects working on rn | done

    # email
    # linkedin
    # other contact info
    # the github stats i fetched

    # then below the snake, num of people who visited



    elements = [
        styles,

        svg.Text(x=370, y=35, fill='333333', class_='ascii', elements = [

            svg.TSpan(x=370, y=35, class_=["category"], text="Andrew Tarasidis"),

            svg.TSpan(dy = dy*2, x = 370, class_=["titles"], text="Info"),
            svg.TSpan(dy = dy, x = 370, text="--------------------"),
            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Uptime"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="FETCHAGEDATA"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Born in"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Greece"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Currently located in"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Ioannina, Greece"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Studies"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Computer Science and Engineering, UOI"),

            svg.TSpan(dy = dy*2, x = 370, class_=["titles"], text="Capabilities"),
            svg.TSpan(dy = dy, x = 370, text="--------------------"),
            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Languages"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="C# | Rust | Python | Java"),
            svg.TSpan(dy = dy, x = 400, class_ = ["extras"], text=" ( Knowledge in: C | C++ | GLSL)"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Interests"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Game Development | Computer Graphics | Software Development"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Currently Working on"),
            svg.TSpan(text=": "),
            svg.TSpan(dy = dy, x = 400, class_ = ["data"], text="Voxel engine with Rust and Vulkano | Desktop app with multiple helper functionalities"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Hobbies"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Drawing | Playing Guitar | Working out | Playing Games | Helping People | Being Kind"),

            svg.TSpan(dy = dy*2, x = 370, class_=["titles"], text="Contact Me"),
            svg.TSpan(dy = dy, x = 370, text="--------------------"),
            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Email"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="andytgamedev@gmail.com"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="LinkedIn"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="in/andreas-tarasidis"),
            ]
        ),
        
    ]

    file = svg.SVG(
        width = svgwidth,
        height = svgheight,
        elements = elements,
    )

    f = open("temp.svg", mode='w', encoding='utf-8')
    f.write(file.as_str())
    f.close()

if __name__ == '__main__':

    createSvgData()

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


