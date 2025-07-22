'''
Inspired by GitHub user 'Andrew6rant's README.
Their profile link : https://github.com/Andrew6rant
Their README repo link : https://github.com/Andrew6rant/Andrew6rant
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

HEADERS = {'authorization': 'token '+ os.environ['ACCESS_TOKEN']}
USER_NAME = os.environ['USER_NAME'] # 'AndreasTar'

QUERY_COUNT = {
    'fetchUserData': 0,
    'fetchStars': 0,
    'fetchCommits': 0
}




profile1 = """                        .....              
               ..+#+.+#######+-.           
            .-##################+-.        
           .+#####################+.       
          .########################-       
         .############++++++#######+.      
         .#####+--....    ....-+###.       
         -###--...          ...-###-       
         .##+--....       .....+####       
         +##++++-..   ..-++++-..+###.      
        .####++##+-...-----...-..+##.      
        .#++######+-...+###++....+#+.      
        -#+-++-+++--....--..   ..-#-..     
        ++--...-+--......      ...-...     
        -+--..--+#-..--....   .. .--..     
        .#+--######+##+++--- ....-...      
        .+#--####+--....-#+-....-...       
         .##+#--++--......-....---         
          .####++++++-...-.------.         
           .####+++++---+++++++..          
             +######++-+#####-.. .         
              ##########++--.......        
              -++---................       
              .++--...................     
              .---...................--..  
          .-+##----...........--++########.
     -+#########-+#########################
     ######################################"""

profile2 = """                           .  .                   
                  .!J!.^JPGGPP5PY~:.             
              .!5G&&@&&&&&&&&&&###BP7^           
             !G#&&&&&&&&&&&&&&&&&##BGYY.         
           :B&&&&@@&@@&&@@&&&&&@@&&#&##?         
           B&@@@&&#GP555Y??????YPB&&##GY.        
          .#@@&PJ~:.... .       ..^Y##B7         
          .#&G~:...                :Y##Y         
          .&B!:....               .~5BBB:        
          J&5JJJ?!:..     .^!!!!~^..!PGG^        
          #GP5YYY5Y?^.  ..^77!^::::  ^BP:        
         :&J7?5Y5YYY?:   .!7J?!^:    ^GP~        
         ?B~~!!!~~!!~.   ..:.....    ^G7..       
        .YJ^:....^~~.                .7  .       
         7?~:...:!?J~..::..          ..:..       
         !5!:.YP55PP57YJ7!~~~^~.     ....        
         .Y5~:JJ5P7~^......!YJ~.   ..:           
           GBJJ!^!!~:.........  ....~^           
           .B&&G!~!7!!~^.  .:..^~~^^:.           
             J&&GJ7?7!~^:.^~?J?JY?~.             
              .#&#GP5Y?777Y5GGG5?:               
               ^GBBGGGP5YYJ77~^.     .           
                ?J7~::......         ..          
                ~!~^..               ....        
                ~~^:.. ..              ..^   
           :~?G#?:::....       ..:~!?YPB&&@Y
      ?YB#&@@@@@&5?Y5PGGGGB###&&&@@@@@@@@@@B
      G&&@@@&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

profile3 = """                        .:. ..                  
               .....:^:^~!~~!77~:               
           :!~~^^::^^^^:^^^^~~!!!!7:            
         .:!!^^::::::^^:::::^^^~!7JJ^           
        .^^^^:::::.:::::::::.::^^^^~!.          
        ^::::::~!77??JYYJYYJ?7!^^~~!?:          
       :^:.^7J5GBB#######&&&##BP?~~!?.          
       ^~:75GB###&&&&&&&&&&&&&&#G?~~7:          
       .:~5BB#####&&&&&&&&&&&&&#57!~!~          
       .^?JJJY5GB#&&&&##P5555PG##57!7!          
       .!7??????YP#&&BBG5Y5PGBGG&@P!?!          
       :JYY??????YG&&&B5YJJ5PG&&&@P!?J.         
      :~PP55555555B####BBBB###&&&@G!Y#GJ        
     :JJPBB##BGPPB&&&###&###&&&&&@#Y&&#G        
     .JYPB##BG5JJPBBGBB####&&&&@@@#BB#B^        
      ?J5BB?77777?YJJY5PPPPP#&&@&&B##&7         
      ^!?5GJJ?7Y5GB####B5?JP#&&&#BGBG?          
        ~!JJ5G55PGB#######B##B##BPJ.            
        .^^^!5P5555PGB&&#GBBGPPGGG~             
          .:^!J5YY55PGBGPYJJJJJ5#&.             
           .::^!7??YYYYJ?!!!?YG#@@?             
            ^7!!!!!7???JY5PGB&&&&@#7            
            .JJYPGBB######&&&&&&&###J.          
             ?55GB#####&&&&&&&&&&####G7:        
             7PGGB#####&&&@@@@@&&&&&#BGY!.   
          ..:YGGBB####&&&&&##BGP5Y?7~^:::::
     :.....:.:?Y??7!!!!!~~^^:::.............
     ^:.::^^:................:::::::........"""

PROFILE_TEXT = profile3.replace("&","&amp;").replace(">","&gt;").replace("<","&lt;").splitlines()

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
    the input dates (MAX date differential: 1 year)
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
    Prints a formatted time differential for performance metrics.\n
    Returns formatted result if whitespace is specified, otherwise returns raw result
    """
    print('{:<27}'.format('   ' + query_type + ':'), sep='', end='')
    print('{:>12}'.format('%.4f' % difference + ' s ')) if difference > 1 else print('{:>12}'.format('%.4f' % (difference * 1000) + ' ms'))
    if whitespace:
        return f"{'{:,}'.format(funct_return): <{whitespace}}"
    return funct_return

def createSvgData(age, commits, stars):

    svgwidth = 970
    svgheight = 620

    dy = 20

    styles = svg.Style(
        text = dedent("""
                      .titles { fill: #3EFF01 }
                      .category { fill: #FF9536 }
                      .data { fill: #8FE9FF }
                      .extras { fill: #AAAAAA }
                      .hidden { fill: #757575 }
                      .profile { fill: #E3DCE9; white-space: pre }
                      text, tspan { font-family: Consolas; font-size: 94%; fill: #BBBBBB }
                      """), 
    )

    # IDEA on top of the readme, a procedural ascii day-night cycle scene

    # i want to have:

    # date of birth | done
    # where i live | done
    # degree / uni | done

    # languages | done
    # hobbies | done
    # interests | done
    # projects working on rn | done

    # email | done
    # linkedin | done
    # other contact info
    # the github stats i fetched | done

    # then below the snake

    elements = [
        styles,

        svg.Rect(width=svgwidth, height=svgheight, fill="#111111", rx=15),
        svg.Text(x=370, y=35, fill='#333333', class_='ascii', elements = [

            svg.TSpan(x=370, y=35, class_=["category"], font_weight="bolder" ,text="Andreas Tarasidis"),

            # ------------------------------------------------------------------------------

            svg.TSpan(dy = dy*2, x = 370, class_=["titles"], text="Info"),
            svg.TSpan(dy = dy, x = 370, text="--------------------"),
            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Uptime"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text=age),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Born in"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Greece"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Currently located in"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Ioannina, Greece"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Studies"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Computer Science and Engineering, UOI"),

            # ------------------------------------------------------------------------------

            svg.TSpan(dy = dy*2, x = 370, class_=["titles"], text="Capabilities"),
            svg.TSpan(dy = dy, x = 370, text="--------------------"),
            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Languages"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="C# | Rust | Python | Java | C++ | C | GLSL"),
            svg.TSpan(dy = dy, x = 400, class_ = ["extras"], text="( Knowledge in: Verilog | VHDL | Assembly | Octave)"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Interests"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Game Development | Computer Graphics | Software Development"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Currently Working on"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text=" "),
            svg.TSpan(dy = dy, x = 400, class_ = ["data"], text="| Voxel engine with Rust and Vulkano"),
            svg.TSpan(dy = dy, x = 400, class_ = ["data"], text="| Desktop app with multiple helper functionalities with Rust and iced"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Hobbies"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="Drawing | Playing Guitar | Working out | Video Games |"),
            svg.TSpan(dy = dy, x = 440, class_ = ["data"], text="Helping People | Being Kind | Improving Myself"),

            # ------------------------------------------------------------------------------

            svg.TSpan(dy = dy*2, x = 370, class_=["titles"], text="Contact Me"),
            svg.TSpan(dy = dy, x = 370, text="--------------------"),
            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Email"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="andreas.tarasidis@gmail.com"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="LinkedIn"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text="in/andreas-tarasidis"),

            # ------------------------------------------------------------------------------

            svg.TSpan(dy = dy*2, x = 370, class_=["titles"], text="Github Stats"),
            svg.TSpan(dy = dy, x = 370, text="--------------------"),
            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Commits"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text=commits),
            svg.TSpan(class_ = ["extras"], text=" ( Past 365 days )"),
            svg.TSpan(class_ = ["hidden"], text=" Updates every Sunday"),

            svg.TSpan(dy = dy, x = 370, class_ = ["category"], text="Total Stars"),
            svg.TSpan(text=": "),
            svg.TSpan(class_ = ["data"], text=stars),



            svg.TSpan(x=0, y=55,  class_='profile', text=PROFILE_TEXT[0]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[1]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[2]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[3]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[4]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[5]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[6]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[7]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[8]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[9]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[10]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[11]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[12]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[13]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[14]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[15]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[16]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[17]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[18]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[19]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[20]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[21]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[22]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[23]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[24]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[25]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[26]),
            svg.TSpan(x=0, dy=dy, class_='profile', text=PROFILE_TEXT[27]),
            ]
        )
        
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

    userData, fetchUserTime = _performanceCounter(fetchUserData, USER_NAME)
    _formatData('account data', fetchUserTime)

    # user id and create at time X
    userID, userCreatedData = userData

    ageData, ageCalculatorTime = _performanceCounter(ageCalculator)
    _formatData('age data (internal)', ageCalculatorTime)

    #userCreatedData, datetime.datetime.now().replace(microsecond=0).isoformat()+'Z'
    commitData, fetchCommitsTime = _performanceCounter(fetchCommits)
    _formatData('commits data', fetchCommitsTime, commitData)

    starsData, fetchStarsTime = _performanceCounter(fetchStars)
    _formatData('stars data', fetchStarsTime, starsData)
    _, starsData = starsData

    createSvgData(ageData, commitData, starsData)


