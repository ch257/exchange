import urllib.request
url = 'http://export.finam.ru/SPFB.Eu-3.19_190108_190108.txt?market=14&em=487593&code=SPFB.Eu-3.19&apply=0&df=8&mf=0&yf=2019&from=08.01.2019&dt=8&mt=0&yt=2019&to=08.01.2019&p=3&f=SPFB.Eu-3.19_190108_190108&e=.txt&cn=SPFB.Eu-3.19&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
page = urllib.request.urlopen(url)
content = page.read()

print(content)


# request = urllib.request.Request('http://mysite/admin/index.cgi?index=127')
# base64string = base64.b64encode(bytes('%s:%s' % ('login', 'password'),'ascii'))
# request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
# result = urllib.request.urlopen(request)
# resulttext = result.read()
# import urllib.request
# with urllib.request.urlopen('http://python.org/') as response:
   # html = response.read()