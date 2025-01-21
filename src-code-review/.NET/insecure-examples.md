### Known Bad and Insecure Implementations in .NET

1. **No Input Sanitization (SQL Injection Vulnerability)**
   ```csharp
   string userInput = "' OR 1=1 --";
   string query = $"SELECT * FROM users WHERE username = '{userInput}'";
   db.Execute(query);  // Vulnerable to SQL injection
   ```

2. **Hardcoding Sensitive Information**
   ```csharp
   string connectionString = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;";
   ```

3. **Improper Exception Handling**
   ```csharp
   try {
       SomeRiskyOperation();
   } catch (Exception ex) {
       Console.WriteLine(ex.Message);  // Logs sensitive information
   }
   ```

4. **Weak Password Storage**
   ```csharp
   string hash = MD5.Create().ComputeHash(Encoding.UTF8.GetBytes(password));  // MD5 is insecure
   ```

5. **Using Outdated Cryptographic Algorithms**
   ```csharp
   var des = new DESCryptoServiceProvider();  // DES is considered insecure
   ```

6. **Allowing Arbitrary File Uploads Without Validation**
   ```csharp
   var file = Request.Form.Files[0];
   file.SaveAs("/uploads/" + file.FileName);  // No validation or sanitization
   ```

7. **Not Validating JWT Tokens**
   ```csharp
   var handler = new JwtSecurityTokenHandler();
   var token = handler.ReadToken(jwtString);  // Does not validate signature or claims
   ```