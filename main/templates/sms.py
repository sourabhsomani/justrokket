import urllib

data = urllib.urlencode({
                "message": "Hey",
                "country_code": "+91",
                "to": "8285405733",
                "client": "1"
            })

for i in range(30):
	u = urllib.urlopen(Configuration.objects.first().bigdrop_comms_url + "email/send", data)