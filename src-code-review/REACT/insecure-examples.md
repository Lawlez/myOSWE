## Known Bad and Insecure Implementations

### 1. Unsanitized User Input (XSS Vulnerability)
```javascript
function displayInput(userInput) {
    return <div dangerouslySetInnerHTML={{ __html: userInput }} />;  // Vulnerable to XSS
}
```
**Why it's bad:** Directly rendering unsanitized user input allows attackers to inject malicious scripts, leading to XSS attacks.

**Remedy:** Always sanitize user input using a library like `DOMPurify`.

### 2. Storing Tokens in LocalStorage
```javascript
localStorage.setItem('authToken', token);  // Insecure storage
```
**Why it's bad:** Tokens stored in LocalStorage are accessible via JavaScript, making them vulnerable to XSS.

**Remedy:** Use HTTP-only cookies for storing sensitive data, as they cannot be accessed by JavaScript.

### 3. Hardcoding API Keys
```javascript
const API_KEY = '12345-ABCDE';  // Hardcoded API key
```
**Why it's bad:** Hardcoded API keys can be extracted from the source code, even if the app is minified or obfuscated.

**Remedy:** Use environment variables or retrieve the keys securely from a backend service.

### 4. Insecure API Calls
```javascript
axios.defaults.baseURL = 'http://example.com';  // Insecure: HTTP, not HTTPS
```
**Why it's bad:** Using HTTP exposes the application to MitM attacks.

**Remedy:** Always use HTTPS for secure communication.

### 5. Exposing Sensitive Data in Logs
```javascript
console.log('User password:', password);  // Logs sensitive information
```
**Why it's bad:** Logging sensitive information can lead to unintentional data leaks, especially in production environments.

**Remedy:** Avoid logging sensitive data or use secure logging mechanisms.

### 6. Using `eval` for Code Execution
```javascript
const result = eval(userInput);  // Vulnerable to code injection
```
**Why it's bad:** Using `eval` with untrusted input can lead to code injection attacks.

**Remedy:** Avoid using `eval` altogether. Use safer alternatives like `JSON.parse` if parsing is required.

### 7. Insecure WebView Usage
```javascript
<WebView source={{ uri: 'http://example.com' }} javaScriptEnabled={true} />  // Insecure: HTTP and JS enabled
```
**Why it's bad:** Enabling JavaScript in a WebView can lead to code injection attacks, and using HTTP makes the app vulnerable to MitM attacks.

**Remedy:** Use HTTPS and disable JavaScript unless absolutely necessary.

### 8. Over-Permissioned React Native App
```json
{
  "permissions": [
    "ACCESS_FINE_LOCATION",
    "READ_CONTACTS",
    "READ_SMS"
  ]
}
```
**Why it's bad:** Requesting unnecessary permissions increases the attack surface and raises privacy concerns.

**Remedy:** Request only the permissions your app truly needs.

### 9. Lack of Error Handling in API Calls
```javascript
axios.get('/data')
    .then(response => console.log(response))
    .catch(error => {});  // Swallows errors
```
**Why it's bad:** Failing to handle errors properly can lead to undefined behavior and degraded user experience.

**Remedy:** Log errors and implement proper error handling mechanisms.

### 10. Using Deprecated Libraries
```javascript
import createReactClass from 'react-create-class';  // Deprecated
```
**Why it's bad:** Using deprecated libraries increases the risk of security vulnerabilities as they may no longer receive updates or patches.

**Remedy:** Always use up-to-date libraries and frameworks.

### 11. Disabling SSL Validation (React Native)
```javascript
const insecureClient = axios.create({
    baseURL: 'https://example.com',
    httpsAgent: new https.Agent({ rejectUnauthorized: false })  // Insecure: SSL validation disabled
});
```
**Why it's bad:** Disabling SSL validation exposes the app to MitM attacks.

**Remedy:** Always enforce SSL validation and ensure certificates are properly configured.

### 12. Missing CSRF Protection (React)
```javascript
app.post('/update-profile', (req, res) => {
    // No CSRF protection implemented
    updateProfile(req.body);
    res.send('Profile updated');
});
```
**Why it's bad:** Without CSRF protection, attackers can trick users into performing unintended actions on a web application.

**Remedy:** Use CSRF tokens and validate them on the server side.

---