from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

REST_COUNTRIES_API = "https://restcountries.com/v3.1/name"

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        query_params = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
        country_name = query_params.get("country", "").capitalize()
        
        if country_name:
            response = requests.get(f"{REST_COUNTRIES_API}/{country_name}")
            country_info = response.json()[0] if response.status_code == 200 else None
            message = str(country_info) if country_info else "Country not found."
        else:
            message = "Bad Request: Please provide a country parameter."

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

        return
