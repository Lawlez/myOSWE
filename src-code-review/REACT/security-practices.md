### React and React Native Security Review

This guide provides a comprehensive reference for performing secure code reviews in **React** and **React Native** applications. It includes key differences, best practices, and examples of known bad or insecure implementations.


## React vs React Native Summary

### Key Differences
- **React**: A JavaScript library for building user interfaces, primarily used for web applications.
- **React Native**: A framework that allows developers to build native mobile applications using React.

| Feature                   | React                            | React Native                      |
|---------------------------|----------------------------------|-----------------------------------|
| Platform                  | Web                              | iOS, Android                      |
| Rendering Method          | Virtual DOM                      | Native components                 |
| Navigation                | React Router                     | React Navigation                  |
| Styling                   | CSS, CSS-in-JS                   | Stylesheets (similar to CSS)      |
| Storage                   | LocalStorage, SessionStorage     | AsyncStorage, SecureStore         |

---

## Security Features and Best Practices

### 1. Input Sanitization
- **React**: Always sanitize user input before rendering it to prevent Cross-Site Scripting (XSS) attacks. XSS occurs when malicious scripts are injected into web pages and executed in the user’s browser.
  ```javascript
  import DOMPurify from 'dompurify';

  function displayInput(userInput) {
      const sanitizedInput = DOMPurify.sanitize(userInput);
      return <div dangerouslySetInnerHTML={{ __html: sanitizedInput }} />;
  }
  ```
  **Explanation:** The above example uses `DOMPurify` to remove potentially harmful scripts from the input. Without this sanitization, an attacker could inject scripts to steal user data or hijack sessions.

- **React Native**: Input sanitization is equally important when handling dynamic content, especially if using `WebView` components.

### 2. Avoiding `dangerouslySetInnerHTML`
- Using `dangerouslySetInnerHTML` allows inserting raw HTML directly into a React component. This can be dangerous if the HTML contains malicious scripts.
  ```javascript
  // Avoid this unless absolutely necessary
  <div dangerouslySetInnerHTML={{ __html: userProvidedHTML }} />
  ```
  **Best Practice:** If `dangerouslySetInnerHTML` must be used, ensure that the input is thoroughly sanitized beforehand using a library like `DOMPurify`.

### 3. Secure Storage
- **React**: Use `LocalStorage` or `SessionStorage` cautiously, as they are accessible via JavaScript and vulnerable to XSS attacks. Avoid storing sensitive information such as authentication tokens in LocalStorage.

  **Example of insecure storage:**
  ```javascript
  localStorage.setItem('authToken', token);  // Insecure: vulnerable to XSS
  ```

  **Best Practice:** Use HTTP-only cookies for storing sensitive data, as they are not accessible via JavaScript.

- **React Native**: Use secure storage solutions like `SecureStore` (for Expo apps) or `react-native-encrypted-storage` for sensitive information.
  ```javascript
  import EncryptedStorage from 'react-native-encrypted-storage';

  async function storeToken(token) {
      await EncryptedStorage.setItem('authToken', token);
  }
  ```
  **Explanation:** EncryptedStorage provides an additional layer of security by encrypting data before storing it.

### 4. Authentication and Authorization
- **Token Storage**: In React, prefer storing authentication tokens in HTTP-only cookies instead of LocalStorage to mitigate XSS risks.

- **Session Management**: Implement proper session expiration and renewal mechanisms. Use refresh tokens to maintain user sessions securely.
  ```javascript
  axios.interceptors.response.use(
      response => response,
      async error => {
          if (error.response.status === 401) {
              // Refresh the token and retry the request
          }
          return Promise.reject(error);
      }
  );
  ```

### 5. Preventing Insecure API Calls
- Always use HTTPS for API communication to prevent Man-in-the-Middle (MitM) attacks.

- **React Native Specific**: Avoid disabling SSL validation, even in development environments. Disabling SSL validation exposes the app to MitM attacks.
  ```javascript
  axios.defaults.baseURL = 'https://secure-api.example.com';
  ```

### 6. Secure State Management
- Avoid storing sensitive information (e.g., authentication tokens, passwords) in the global state, such as Redux or Context, to reduce the risk of accidental exposure during debugging or state persistence.

  **Example:**
  ```javascript
  const [authToken, setAuthToken] = useState(null);  // Avoid storing tokens in plain state
  ```

  **Best Practice:** Store sensitive data in secure storage and retrieve it when needed.

### 7. Code Obfuscation
- **React Native**: Use Metro bundler’s built-in minification and obfuscation options to make reverse engineering more difficult.
  ```bash
  react-native bundle --platform ios --dev false --minify true
  ```
- For Android, enable ProGuard and configure it to remove unnecessary debug information.
  ```gradle
  android {
      buildTypes {
          release {
              minifyEnabled true
              proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
          }
      }
  }
  ```

### 8. Handling Sensitive Permissions (React Native)
- Always request the minimum set of permissions your app needs. Over-requesting permissions increases the attack surface and raises privacy concerns.
- Use `react-native-permissions` to manage runtime permissions in a secure and user-friendly way.
  ```javascript
  import { request, PERMISSIONS } from 'react-native-permissions';

  async function requestLocationPermission() {
      const result = await request(PERMISSIONS.IOS.LOCATION_WHEN_IN_USE);
      if (result === 'granted') {
          console.log('Location permission granted');
      }
  }
  ```

### 9. Preventing Insecure WebViews
- When using `WebView` components in React Native, disable JavaScript execution unless it is absolutely necessary.
  ```javascript
  <WebView source={{ uri: 'https://example.com' }} javaScriptEnabled={false} />
  ```
- Ensure that only trusted URLs are loaded in the WebView to prevent phishing and code injection attacks.

### 10. Avoiding Hardcoded Secrets
- Never hardcode API keys, secrets, or sensitive configuration data directly in the source code. Use environment variables or retrieve them securely from a backend service.

  **Example of insecure code:**
  ```javascript
  const API_KEY = '12345-ABCDE';  // Hardcoded API key
  ```

  **Best Practice:** Use environment-specific configuration files or secure storage solutions.

  ```javascript
  const API_KEY = process.env.REACT_APP_API_KEY;
  ```

---