# -H "Content-Type: application/json" - adds header that tells server you're sending JSON data.
# -d '{"username": "test", "content": "hello"}' - sets request data.
# Using -d also sets method to POST, so -X POST can be ommited.
curl -H "Content-Type: application/json" -d '{"username": "test", "content": "hello"}' "https://discord.com/api/webhooks/972908013566435378/TOKEN"
