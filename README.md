# link-checker
Link-checker – Test Project
<br/>
**This script takes URL and make validity checks:**
1. Classification validation
2. Robots.txt validation
3. Content validation

**Usage:** link-checker-cli.py [-h] -url URL [-log]

**Sample usage:** python link-checker-cli.py -url habr.com
<br/>
**Sample result:**
<br/>
[(True, 'the website redirects to https'),<br/>
 (False, 'the website rejects robots'),<br/>
 (True, 'the website is not parked')]


You can enable log via [-log] parameter to get more info, like:
* ...log: The protocol is not provided (http or https), fall-back to http!
* ...log: No data retrieved because <urlopen error [Errno -2] Name or service not known>!
* ...log: Markers of parked domain found: {'parking': False, 'parked': False, 'buy': False, 'lease': True, 'domain': False}

