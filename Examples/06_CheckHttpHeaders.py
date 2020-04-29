import re
import requests
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import *


links = [
    "https://cat-sso.firstdata.com",
    "https://online-qa.firstdata.com/login",
    "https://online-qa.firstdata.com/gans",
    "https://online-qa.firstdata.com/esp",
    "https://online-qa.firstdata.com/edp",
]


def check_allowed_methods(url):

    # OPTIONS GET POST HEAD PUT DELETE TRACE CONNECT PATCH
    # expect 403 Forbidden
    payload = {'username': 'bob', 'email': 'bob@bob.com'}
    r = requests.post(url, data=payload, verify=False)
    if 400 <= r.status_code <= 410:
        print "    POST method disabled ", r.status_code

    r = requests.put(url, data=payload, verify=False)
    if not (r.status_code == 403 or r.status_code == 405):
        print "    Enabled unsafe method PUT ", r.status_code

    r = requests.options(url, verify=False)
    if not (r.status_code == 403 or r.status_code == 405):
        print "    Enabled unsafe method OPTIONS", r.status_code

    r = requests.head(url, verify=False)
    if not (r.status_code == 403 or r.status_code == 405):
        print "    Enabled unsafe method HEAD", r.status_code

    r = requests.delete(url, verify=False)
    if not (r.status_code == 403 or r.status_code == 405):
        print "    Enabled unsafe method DELETE", r.status_code

    r = requests.patch(url, data=payload, verify=False)
    if not (r.status_code == 403 or r.status_code == 405):
        print "    Enabled unsafe method PATCH", r.status_code


# def check_header(response, header, expected_value):
#     value = response.headers.get(header)
#     if value == "":
#         print "    Missing HTTP header", header, "in response"
#     elif value != expected_value:
#         print "    Unexpected value of HTTP header", header, ", received:", value, ", expected:", expected_value


def check_header_regex(response, header, regex):
    value = response.headers.get(header)
    if value is None:
        print "    Missing HTTP header", header, "in response"
    else:
        match = regex.match(value)
        if match is None:
            print "    Unexpected value of HTTP header", header, ", received:", value, ", expected:", regex.pattern


header_checks = [
    # HTTP header, Regexp for validation
    ["Server", re.compile("Apache\s*$|\s*$")],
    ["Strict-Transport-Security", re.compile("max-age=\d*; includeSubdomains")],
    ["X-XSS-Protection", re.compile("1; mode=block")],
    ["X-Content-Type-Options", re.compile("nosniff")],
    # ["Content-Security-Policy", re.compile("default-src 'self' 'unsafe-eval' 'unsafe-inline'")],
    ["Cache-Control", re.compile("no-cache, no-store, must-revalidate")],
    ["X-Frame-Options", re.compile("SAMEORIGIN")],
]


def check_headers(r):
    # print "    HTTP headers:", r.headers
    for h in header_checks:
        check_header_regex(r, h[0], h[1])

    # print r.cookies
    for cookie in r.cookies:
        if cookie.secure is False:
            print "    Missing Secure option for cookie", cookie.name
        if cookie.has_nonstandard_attr('HttpOnly') is False:
            print "    Missing HttpOnly option for cookie", cookie.name


def check_content(r):
    if r.status_code != 200:
        print "    Cannot check content of the page - not a 200 response"

    regex = re.compile("antiClickjack\.parentNode\.removeChild")
    match = regex.search(r.content)
    # print r.content
    if match is None:
        print "    Missing antiClickjack script."


urllib3.disable_warnings(InsecureRequestWarning)

for l in links:
    print l
    try:
        r = requests.get(l)
    except SSLError:
        print "    Certificate validation failed"
        r = requests.get(l, verify=False)
    except ConnectionError:
        print "    Connection failed", l
        continue

    if r.status_code == 200:
        check_allowed_methods(l)
        check_headers(r)
        check_content(r)
    else:
        print "    Error getting page", l


