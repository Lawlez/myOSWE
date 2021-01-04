| **Command** | **Description** |
| --------------|-------------------|
| `curl http://inlanefreight.com` | GET request with `cURL` |
| `curl http://inlanefreight.com -v` | Verbose GET request with `cURL` |
| `curl http://admin:password@inlanefreight.com/ -vvv` | `cURL` Basic Auth login |
| `curl -u admin:password  http://inlanefreight.com/ -vvv` | Alternate `cURL` Basic Auth login |
| `curl -u admin:password -L http://inlanefreight.com/` | `cURL` Basic Auth login, follow redirection |
| `curl -u admin:password 'http://inlanefreight.com/search.php?port_code=us'` | `cURL` GET request with parameter |
| `curl -d 'username=admin&password=password' -L http://inlanefreight.com/login.php` | POST request with `cURL` |
| `curl -d 'username=admin&password=password' -L  http://inlanefreight.com/login.php -v` | Debugging with `cURL` |
| `curl -d 'username=admin&password=password' -L --cookie-jar /dev/null  http://inlanefreight.com/login.php -v` | Cookie usage with `cURL` |
| `curl -d 'username=admin&password=password' -L --cookie-jar cookies.txt  http://inlanefreight.com/login.php` | `cURL` with cookie file |
| `curl -H 'Content-Type: application/json' -d '{ "username" : "admin", "password" : "password" }'` | `cURL` specify content type |
| `curl -X OPTIONS http://inlanefreight.com/ -vv` | `cURL` OPTIONS request |
| `curl -X PUT -d @test.txt http://inlanefreight.com/test.txt -vv` | File upload with `cURL` |
| `curl -X DELETE http://inlanefreight.com/test.txt -vv` | DELETE method with `cURL` |