import re

regex = r"^Content-Type:\s(\w+/\w+).*$"

test_str = ("HTTP/1.1 200 OK\n"
	"Date: Fri, 20 May 2022 01:54:23 GMT\n"
	"Server: Apache/2.4.18 (Ubuntu)\n"
	"Vary: Accept-Encoding\n"
	"Cache-Control: max-age=0, no-cache, no-store, must-revalidate\n"
	"Pragma: no-cache\n"
	"Expires: Wed, 11 Jan 1984 05:00:00 GMT\n"
	"Content-Length: 3143\n"
	"Keep-Alive: timeout=5, max=100\n"
	"Connection: Keep-Alive\n"
	"Content-Type: text/html;charset=UTF-8\n\n\n"
	"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">")

matches = re.search(regex, test_str, re.MULTILINE)

print(matches.group(1))

# for matchNum, match in enumerate(matches, start=1):
    
#     print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
#     for groupNum in range(0, len(match.groups())):
#         groupNum = groupNum + 1
        
#         print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))