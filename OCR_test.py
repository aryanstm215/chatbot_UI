import requests
import json

instructions = {
  'parts': [
    {
      'file': 'scanned'
    }
  ],
  'actions': [
    {
      'type': 'ocr',
      'language': 'english'
    }
  ]
}

response = requests.request(
  'POST',
  'https://api.pspdfkit.com/build',
  headers = {
    'Authorization': 'Bearer pdf_live_waa9XMBcfYXbXMw691daAiRkTueALiGnvTasQFXKRyl'
  },
  files = {
    'scanned': open('Aryan_Resume.pdf', 'rb')
  },
  data = {
    'instructions': json.dumps(instructions)
  },
  stream = True
)

if response.ok:
  with open('Aryan_Resume.pdf', 'wb') as fd:
    for chunk in response.iter_content(chunk_size=8096):
      fd.write(chunk)
else:
  print(response.text)
  exit()
