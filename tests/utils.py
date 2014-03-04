import base64

class FlaskTestAuthenticationUtils(object):
	def login_with_credentials_request(self, url, username, password):
		res = self.client.open(url, "GET", 
            headers={
                'Authorization': 'Basic ' + base64.b64encode(username + ":" \
                    + password)
            })

		return res
	