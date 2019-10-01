![Playoff Python SDK](https://dev.playoffgamification.io/images/assets/pl-python-sdk.png "Playoff Python SDK")

Playoff Python SDK [![PyPI version](https://badge.fury.io/py/playoff.svg)](http://badge.fury.io/py/playoff)
=================
This is the official OAuth 2.0 Python client SDK for the Playoff API.
It supports the `client_credentials` and `authorization code` OAuth 2.0 flows.
For a complete API Reference checkout [Playoff Developers](https://dev.playoffgamification.io/docs/api) for more information.

>Note: Breaking Changes this is the new version of the sdk which uses the Playoff api v2 by default if you still want to use the v1 api you can do that so by passing a version param with 'v1'

The Playoff class allows you to make rest api calls like GET, POST, .. etc
ex:
```py
pl = Playoff(
    version = 'v1',
    client_id = "Your client id",
    client_secret = "Your client secret",
    type = 'client'
)
#For v1 api
# To get infomation of the player johny
pl = Playoff(
    version = 'v1',
    client_id = "Your client id",
    client_secret = "Your client secret",
    type = 'client'
  )
player = pl.get(
  route =  '/player',
  query = { 'player_id': 'johny' }
)
print player['id']
print player['scores']

# To get all available processes with query
processes = pl.get(route =  '/processes', query = { player_id: 'johny' })
print processes
# To start a process
process =  pl.post(
  route =  "/definitions/processes/collect",
  query = { 'player_id': 'johny' },
  body = { 'name': "My First Process" }
)

#To play a process
pl.post(
  route =  "/processes/%s/play" %process_id,
  query = { 'player_id': 'johny' },
  body = { 'trigger': "#{@trigger}" }
)
#For v2 api
```python
# To get infomation of the player johny
pl = Playoff(
    client_id = "Your client id",
    client_secret = "Your client secret",
    type = 'client'
  )
player = pl.get(
  route =  '/runtime/player',
  query = { 'player_id': 'johny' }
)
print player['id']
print player['scores']
```

Requires
--------
Python 2.7.6

Install
----------
```python
pip install playoff
```
or if you are using django or flask
Just add it to your requirements.txt file
```python
playoff==0.7.4
```
and do a pip install -r requirements.txt

Using
-----
### Create a client
  If you haven't created a client for your game yet just head over to [Playoff](https://playoffgamification.io) and login into your account, and go to the game settings and click on client.

## 1. Client Credentials Flow
In the client page select Yes for both the first and second questions
![client](https://dev.playoffgamification.io/images/assets/client.png)

A typical flask app using client credentials code flow with a single route would look something like this
```python
@app.route("/client")
def client():
  pl = Playoff(
    client_id = "Your client id",
    client_secret = "Your client secret",
    type = 'client'
  )
  players = pl.get(route = '/admin/players')
  html = "<ul>"
  for player in players['data']:
    html += "<li>" + str(player['alias']) + "</li>"
  html+= "</ul>"
  return html
```

## 2. Authorization Code Flow
In the client page select yes for the first question and no for the second
![auth](https://dev.playoffgamification.io/images/assets/auth.png)

In this flow you will have a controller which will get the authorization code and using this the sdk can get the access token. You need a view which will allow your user to login using the playoff platform. And then playoff server with make a get request with the code to your redirect uri. And you should find the code in the query params or the url and exchange the code with the Playoff SDK.
```python
exchange_code(code)
```

Now you should be able to access the Playoff api across all your
controllers.
```python
@app.route("/login")
def login():
  global pl
  pl = Playoff(
    client_id = "YmE1MDQzMmUtMmU4MC00YWU4LWEyZGMtODJiMDQ3NGY2NDNh",
    client_secret = "ZTczNTM3N2UtMmE3MS00ZDdkLWI4NzctZjM3ZDFjZGI5ZGQ4YjM0Y2ViNTAtNTg1My0xMWU0LWE4MDEtZjkwOTJkZGEwOWUz",
    type = 'code',
    redirect_uri = 'http://127.0.0.1:5000/code'
  )
  if 'username' in session:
    return redirect(url_for('home'))
  else:
    url = pl.get_login_url()
    return """
      <h2> Please Login to your Playoff Account </h1>
      <h2><a href="%s">Login</a></h2>
    """ %url

@app.route("/code")
def code():
  global pl
  params = request.args.items()
  if params[0][1] != None:
    pl.exchange_code(params[0][1])
    session['username'] = "user1"
    return redirect(url_for('home'))
  else:
    return redirect(url_for('login'))
  return ""

@app.route("/home")
def home():
  global pl
  if 'username' in session:
    players = pl.get(route = '/admin/players')
    html = "<ul>"
    for player in players['data']:
      html += "<li>" + str(player['alias']) + "</li>"
    html+= "</ul>"
    html+= "<a href=\"/logout\"> Sign out</a>"
    return html
  else:
    return 'You are not logged in'

@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for('login'))
```

## 3. Custom Login Flow using JWT(JSON Web Token)
In the client page select no for the first question and yes for the second
![jwt](https://dev.playoffgamification.io/images/assets/jwt.png)
```python
token = Playoff.createJWT(
    client_id = 'your client_id', 
    client_secret = 'your client_secret', 
    player_id = 'johny', // The player id associated with your user
    scopes = ['player.runtime.read', 'player.runtime.write'], // The scopes the player has access to
    expires = 3600; // 1 hour
})
```

This is used to create jwt token which can be created when your user is authenticated. This token can then be sent to the frontend and or stored in your session. With this token the user can directly send requests to the Playoff API as the player.

# Client Scopes
![Client](https://dev.playoffgamification.io/images/assets/client-scopes.png)

Your client has certain access control restrictions. There are 3 kind of resources in the Playoff REST API they are,

1.`/admin` -> routes for you to perform admin actions like making a player join a team

2.`/design` -> routes for you to make design changes programmatically

3.`/runtime` -> routes which the users will generally use like getting a player profile, playing an action

The resources accessible to this client can be configured to have a read permission that means only `GET` requests will work.

The resources accessible to this client can be configured to have a write permission that means only `POST`, `PATCH`, `PUT`, `DELETE` requests will work.

The version restriction is only for the design resource and can be used to restrict the client from accessing any version of the game design other than the one specified. By default it allows all.

If access to a route is not allowed and then you make a request to that route then you will get an error like this,
```json
{
  "error": "access_denied",
  "error_description": "You are not allowed to access this api route"
}
```

# Documentation
You can initiate a client by giving the client_id and client_secret params
```python
Playoff(
    client_id = 'Your client id'
    client_secret = 'Your client Secret'
    type = 'client' or 'code'
    redirect_uri = 'The url to redirect to' #only for auth code flow
    store = lambda token: redis.store(token) # The lambda which will persist the access token to a database. You have to persist the token to a database if you want the access token to remain the same in every request
    load = lambda: return redis.get(token) # The lambda which will load the access token. This is called internally by the sdk on every request so the 
    #the access token can be persisted between requests
)
```
In development the sdk caches the access token in memory so you don't need to provide the store and load lambdas. But in production it is highly recommended to persist the token to a database. It is very simple and easy to do it with redis. You can see the test cases for more examples.
You can either use `lambdas` or `methods` for the store and load functions

```python
    import redis
    from playoff import Playoff, PlayoffException
    import json

    def my_store(access_token):
      print 'This will store the token to a databse'
      redis.set('token', json.dumps(token))

    def my_loader():
      print 'The access token will be loaded by the sdk for each request'
      return json.loads(redis.get('token'))

    redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    Playoff(
      client_id = "Your client id",
      client_secret = "Your client secret",
      type = 'client',
      store = lambda token: redis.set('token', json.dumps(token)),
      load = lambda: return json.loads(redis.get('token'))
    )
    # OR
    Playoff(
      client_id = "Your client id",
      client_secret = "Your client secret",
      type = 'client',
      store = my_store,
      load = my_loader
    )
```
**API**
```python
api(
    method = 'GET' # The request method can be GET/POST/PUT/PATCH/DELETE
    route =  '' # The api route to get data from
    query = {} # The query params that you want to send to the route
    raw = False # Whether you want the response to be in raw string form or json
)
```

**Get**
```python
get(
    route =  '' # The api route to get data from
    query = {} # The query params that you want to send to the route
    raw = False # Whether you want the response to be in raw string form or json
)
```
**Post**
```python
post(
    route =  '' # The api route to post data to
    query = {} # The query params that you want to send to the route
    body = {} # The data you want to post to the api this will be automagically converted to json
)
```
**Patch**
```python
patch(
    route =  '' # The api route to patch data
    query = {} # The query params that you want to send to the route
    body = {} # The data you want to update in the api this will be automagically converted to json
)
```
**Put**
```python
put(
    route =  '' # The api route to put data
    query = {} # The query params that you want to send to the route
    body = {} # The data you want to update in the api this will be automagically converted to json
)
```
**Delete**
```python
delete(
    route =  '' # The api route to delete the component
    query = {} # The query params that you want to send to the route
)
```
**Get Login Url**
```python
get_login_url()
#This will return the url to which the user needs to be redirected for the user to login. You can use this directly in your views.
```

**Exchange Code**
```python
exchange_code(code)
#This is used in the auth code flow so that the sdk can get the access token.
#Before any request to the playoff api is made this has to be called atleast once. 
#This should be called in the the route/controller which you specified in your redirect_uri
```

**Errors**  
A ```PlayoffException``` is thrown whenever an error occurs in each call.The Error contains a name and message field which can be used to determine the type of error that occurred.

License
=======
Playoff Python SDK v0.7.4  
https://dev.playoffgamification.io/  
Copyright(c) 2019, Officina S.r.l., support@playoffgamification.io  

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
