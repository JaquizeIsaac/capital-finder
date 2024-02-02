from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        path = self.path
        url_components = parse.urlparse(path)
        query = parse.parse_qs(url_components.query)
        
        country = query.get('country', [])
        capital = query.get('capital', [])
        
        message = ''
        base_url = "https://restcountries.com/v3.1/"
        
        try:
            if country:
                country_name, capital_name = self.get_country_info(base_url + "name/", country[0])
                message = f'The capital of {country_name} is {capital_name}'
                
            elif capital:
                capital_name, country_name = self.get_country_info(base_url + "capital/", capital[0])
                message = f'{capital_name} is indeed the capital of {country_name}'
            
            else:
                message = "Bad Request: Please provide a country or capital parameter."
                
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
    
    def get_country_info(self, url, name):
        response = requests.get(url + name)
        data = response.json()
        return name, data[0]['capital'][0]
