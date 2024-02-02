from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        path = self.path
        url_components = parse.urlparse(path)
        query = parse.parse_qs(url_components.query)
        
        country = query.get('country')
        capital = query.get('capital')
        
        message = ''
        url = "https://restcountries.com/v3.1/name/"
        
        try:
            if country:
                country_name = country[0]
                response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
                data = response.json()
                capital_name = data[0]['capital'][0]
                message = f'The capital of {country_name} is {capital_name}'
                
            elif capital:
                capital_name = capital[0]
                response = requests.get(f"https://restcountries.com/v3.1/capital/{capital_name}")
                data = response.json()
                country_name = data[0]['name']['common']
                message = f'{capital_name} is indeed the capital of {country_name}'
            
            else:
                print("No you're wrong")
                
        except requests.RequestException as e:
            self.send_error(500, f"Server Error: {e}")
            return
        
        except KeyError:
            self.send_error(404, "Data decided to stay home")
            return
        
        except Exception as e:
            self.send_error(500, f"Unexpected server error: {e}")
            return
            
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())
        return