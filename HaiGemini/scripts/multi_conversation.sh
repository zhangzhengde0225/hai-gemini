curl https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$GOOGLE_API_KEY \
    -x http://localhost:8118 \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [
        {"role":"user",
         "parts":[{
           "text": "Write the first line of a story about a magic backpack."}]},
        {"role": "model",
         "parts":[{
           "text": "In the bustling city of Meadow brook, lived a young girl named Sophie. She was a bright and curious soul with an imaginative mind."}]},
        {"role": "user",
         "parts":[{
           "text": "Can you set it in a quiet village in 1600s France?"}]},
      ]
    }' 2> /dev/null | grep "text"