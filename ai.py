#https://youtu.be/VTx0xBPOv5Q

import os
import openai

OPENAI_API_KEY = ""

openai.api_key = OPENAI_API_KEY

#openai.api_key = os.getenv(OPENAI_API_KEY)

response = openai.Completion.create(
  model="text-davinci-002",
  prompt="Please write a short op-ed around 500 words. Keep the language simple and concise. Focus on image processing and hyper image resolution using AI.  Also focus on some practical examples.",
  temperature=0.7,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print (response.choices[0].text)