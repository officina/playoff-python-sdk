import socket
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import json
import time
import jwt
import datetime
from urllib.error import URLError, HTTPError

import ssl



socket.setdefaulttimeout(60)

class PlayoffException(Exception):

  def __init__(self, error, error_description):
    self.name = error
    self.message = error_description
    self.msg = error_description

  def __str__(self):
    return "%s %s" %(self.name, self.message)

class Playoff:
  hostname = 'playoff.cc'
  client_id = ''
  client_secret = ''
  type = ''
  store = None
  load = None
  redirect_uri = ''
  code = None

  @staticmethod
  def createJWT(client_id, client_secret, player_id, scopes = [], expires = 3600):
    token = jwt.encode({'player_id': player_id, 'scopes': scopes, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)}, client_secret, algorithm='HS256')
    token = client_id + ':' + str(token.decode('utf8'))
    return token

  def __init__(self, client_id, client_secret, type, redirect_uri='', store=None, load=None, version='v2', hostname='playoff.cc', allow_unsecure=False):
    self.version = version
    self.client_id = client_id
    self.client_secret = client_secret
    self.type = type
    self.store = store
    self.load = load
    self.hostname = hostname
    if allow_unsecure:
      ssl._create_default_https_context = ssl._create_unverified_context
    if store == None:
      self.store = lambda access_token: ''

  def get_access_token(self):
    headers = { 'Accept': 'text/json'}
    if self.type == 'client':
      data = urllib.parse.urlencode({ 'client_id': self.client_id, 'client_secret': self.client_secret, 'grant_type': 'client_credentials'}).encode("utf-8")
    else:
      data = urllib.parse.urlencode({ 'client_id': self.client_id, 'client_secret': self.client_secret,
        'grant_type': 'authorization_code', 'redirect_uri': self.redirect_uri, 'code': self.code
      }).encode("utf-8")
    req = urllib.request.Request('https://'+self.hostname+'/auth/token', data, headers)
    try:
      response = urllib.request.urlopen(req).read()
    except URLError as e:
      err = json.loads(e.read())
      e.close()
      raise PlayoffException(err['error'], err['error_description'])
    token =json.loads(response)
    token['expires_at'] = int(round(time.time())) + int(token['expires_in'])
    del token['expires_in']
    self.store(token)
    if self.load == None:
      self.load = lambda: token

  def api(self, method='GET', route='', query = {}, body={}, raw=False, retry_flag=False):
    access_token = self.load()
    if int(round(time.time())) >= int(access_token['expires_at']):
      print('Access Token Expired')
      self.get_access_token()
      access_token = self.load()
    query['access_token'] = access_token['access_token']
    headers = { 'Accept': 'text/json', 'Content-Type': 'application/json' }
    req = urllib.request.Request("https://api."+ self.hostname +"/%s%s?%s" %(self.version, route, urllib.parse.urlencode(query)), json.dumps(body).encode("utf-8"), headers)
    req.get_method = lambda: method.upper()
    response = ''
    try:
      response = urllib.request.urlopen(req)
      if raw == True:
        raw_data = response.read()
        response.close()
        return raw_data
      else:
        json_data = json.loads(response.read())
        response.close()
        return json_data
    except HTTPError as e:
      err = json.loads(e.read())
      e.close()
      if err['error'] == 'invalid_access_token':
        self.get_access_token()
        if not retry_flag:
          return self.api(method, route, query, body, raw, True)
      raise PlayoffException(err['error'], err['error_description'])
    except URLError as e:
      err = json.loads(e.read())
      e.close()
      raise PlayoffException(err['error'], err['error_description'])

  def get(self, route='', query={}, raw=False):
    return self.api('GET', route, query, {}, raw)

  def post(self, route='', query={}, body={}):
    return self.api('POST', route, query, body)

  def put(self, route='', query={}, body={}):
    return self.api('PUT', route, query, body)

  def patch(self, route='', query={}, body={}):
    return self.api('PATCH', route, query, body)

  def delete(self, route='', query={}, body={}):
    return self.api('DELETE', route, query)

  def get_login_url(self):
    query = urllib.parse.urlencode({ 'response_type': 'code', 'redirect_uri': self.redirect_uri, 'client_id': self.client_id }).encode("utf-8")
    return "https://" + self.hostname + "/auth?%s" %query

  def exchange_code(self, code):
    self.code = code
    self.get_access_token()
