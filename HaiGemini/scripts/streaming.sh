curl https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:streamGenerateContent?key=${GOOGLE_API_KEY} \
        -x http://localhost:8118 \
        -H 'Content-Type: application/json' \
        --no-buffer \
        -d '{ "contents":[{"parts":[{"text": "写一个快速排序算法，以`写完了`结束."}]}]}' \
        2> /dev/null | grep "text"