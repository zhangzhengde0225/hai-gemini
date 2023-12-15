curl https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:countTokens?key=$GOOGLE_API_KEY \
    -x http://localhost:8118 \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{
          "text": "Write a story about a magic backpack."}]}]}' > response.json