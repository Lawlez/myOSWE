**Known Bad and Insecure Implementations in Swift **

### 1. No Input Sanitization (SQL Injection Vulnerability)
**Context:** Failing to sanitize user input before constructing SQL queries makes the app vulnerable to SQL injection attacks.
```swift
let userInput = "' OR 1=1 --"
let query = "SELECT * FROM users WHERE username = '\(userInput)'"
db.execute(query)  // Vulnerable to SQL injection
```
**Issue:** The query is directly concatenated with user input, allowing malicious users to manipulate it.
**Solution:** Use parameterized queries to prevent SQL injection.

---

### 2. Using Forced Unwrapping Without Checking for nil
**Context:** Forced unwrapping without checking if an optional has a value can cause runtime crashes.
```swift
var name: String? = nil
print(name!)  // Causes runtime crash if name is nil
```
**Issue:** If `name` is nil, this will result in a fatal error.
**Solution:** Use optional binding (`if let`) or optional chaining to safely unwrap.

---

### 3. Storing Sensitive Data in Plain Text
**Context:** Storing sensitive information like passwords in plain text is insecure and can lead to data breaches.
```swift
let password = "superSecret123"
UserDefaults.standard.set(password, forKey: "password")  // Insecure storage
```
**Issue:** UserDefaults is not encrypted, making it easy for attackers to extract sensitive data.
**Solution:** Use the iOS Keychain to store sensitive information securely.

---

### 4. Not Using HTTPS for Network Requests
**Context:** Sending data over HTTP transmits it in plaintext, which can be intercepted by attackers.
```swift
let url = URL(string: "http://example.com")!
let task = URLSession.shared.dataTask(with: url) { data, response, error in
    // Insecure: Data transmitted without encryption
}
task.resume()
```
**Issue:** HTTP does not encrypt data in transit.
**Solution:** Always use HTTPS to ensure data is encrypted.

---

### 5. Ignoring Errors
**Context:** Silently ignoring errors can lead to unexpected behavior and security issues.
```swift
func riskyOperation() throws {
    throw NSError(domain: "Risk", code: 1, userInfo: nil)
}

try? riskyOperation()  // Silently ignores errors
```
**Issue:** Ignoring errors prevents proper error handling and can lead to unpredictable behavior.
**Solution:** Use `do-try-catch` to handle errors explicitly.

---

### 6. Incorrect Use of Weak References (Leads to Memory Leak)
**Context:** Incorrect use of strong references between objects can lead to memory leaks.
```swift
class Owner {
    var pet: Pet?
}

class Pet {
    var owner: Owner?  // Strong reference cycle
}
```
**Issue:** A strong reference cycle prevents both objects from being deallocated.
**Solution:** Use `weak` or `unowned` references to break the cycle.

---

### 7. Exposing Internal APIs
**Context:** Making internal methods public unnecessarily increases the attack surface.
```swift
public func internalMethod() {
    print("Internal functionality exposed")
}
```
**Issue:** Public APIs can be accessed by anyone, which may expose sensitive functionality.
**Solution:** Restrict access by using appropriate access control (`internal`, `private`).

---

### 8. Hardcoding API Keys
**Context:** Hardcoding API keys in the source code makes them easy to extract from the compiled binary.
```swift
let apiKey = "12345-ABCDE"  // Easily extracted from binary
```
**Issue:** Attackers can decompile the app and retrieve the key.
**Solution:** Use secure storage (e.g., Keychain) or a backend service to retrieve API keys.

---

### 9. Using MD5 for Password Hashing
**Context:** MD5 is considered cryptographically weak and should not be used for password hashing.
```swift
import CryptoKit
let hash = Insecure.MD5.hash(data: "password".data(using: .utf8)!)
print(hash)  // MD5 is considered weak and insecure
```
**Issue:** MD5 is vulnerable to collisions and brute-force attacks.
**Solution:** Use a strong hashing algorithm like SHA-256 with a salt.

---

### 10. Performing UI Updates on Background Thread
**Context:** Updating the UI from a background thread can lead to undefined behavior and crashes.
```swift
DispatchQueue.global().async {
    // Incorrect: UI updates must be on main thread
    label.text = "Updated"
}
```
**Issue:** UI updates must always be performed on the main thread.
**Solution:** Use `DispatchQueue.main.async` to ensure UI updates are done on the main thread.

---

### 11. Using Deprecated APIs
**Context:** Using deprecated APIs can introduce compatibility issues and potential vulnerabilities.
```swift
let manager = FileManager()
manager.createFile(atPath: "/tmp/file", contents: nil, attributes: nil)  // Deprecated API usage
```
**Issue:** Deprecated APIs may not receive security patches or updates.
**Solution:** Always use the latest recommended APIs.

---

### 12. Disabling ATS (App Transport Security)
**Context:** Disabling ATS allows insecure connections, making the app vulnerable to attacks.
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```
**Issue:** Allowing arbitrary loads bypasses HTTPS enforcement.
**Solution:** Keep ATS enabled and only allow exceptions for trusted domains.

---

### 13. Improper Exception Handling
**Context:** Using exceptions for flow control can lead to unpredictable behavior and bugs.
```swift
do {
    try someFunction()
} catch {
    throw error  // Re-throwing without handling
}
```
**Issue:** Exceptions should be handled properly instead of re-throwing indiscriminately.
**Solution:** Catch specific errors and handle them appropriately.

---

### 14. Logging Sensitive Information
**Context:** Logging sensitive data can lead to unintentional information disclosure.
```swift
print("User password: \(password)")  // Logs sensitive information
```
**Issue:** Logs can be accessed by attackers, especially in production.
**Solution:** Avoid logging sensitive information or use secure logging mechanisms.

---

### 15. Incorrect Use of Insecure Random Number Generators
**Context:** Using predictable random numbers can lead to weak cryptographic operations.
```swift
let randomNumber = Int(arc4random())  // Insecure random number generation
```
**Issue:** `arc4random` is not cryptographically secure.
**Solution:** Use `CryptoKit` or `SecRandomCopyBytes` for secure random numbers.

---