import base64


def authentication(key):
   credentials = {
        'Bitrix': 'aHR0cHM6Ly92YzFjLmJpdHJpeDI0LnJ1L3Jlc3QvNDc5L21qbWRpNXczd3ZsOWpvNWcvCg==',
       # 'Google': 'Yml0cml4MjQtZGF0YS1zdHVkaW8tMjI3OGM3YmZiMWE3Lmpzb24=',
      #  'Chat-bot': 'aHR0cHM6Ly92YzRkay5iaXRyaXgyNC5ydS9yZXN0LzEvYWZzYmttMzB3MWlwN2Mxei8K',
     #   'Checko': 'ak13N0NJSUlKdE9LU05VYg=='
    }
   return base64.b64decode(credentials[key]).decode('utf-8')
  #  return (credentials[key])
