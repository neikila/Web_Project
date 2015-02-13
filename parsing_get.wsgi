#! /usr/bin/env python


def application(environ, start_response):

   response_body = "Hello world\n"
   param = environ['QUERY_STRING']
   param = param.replace('&', '\n') 
   response_body = response_body+param 
   status = '200 OK'
   response_headers = [('Content-Type', 'text/plain'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)

   return [response_body]
