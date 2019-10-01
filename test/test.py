import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from playoff import Playoff, PlayoffException

client_id = 'clientid'
client_secret  ='clientsecret'

def test_wrong_init():
  try:
    pl = Playoff(
      version = 'v1',
      client_id = "wrong_id",
      client_secret = "wrong_secret",
      type = 'client'
    )
  except PlayoffException as e:
    assert 'Client authentication failed' in e.message

def test_v1():
  pl = Playoff(
    version = 'v1',
    client_id = client_id,
    client_secret = client_secret,
    type = 'client'
  )

  try:
    pl.get(route= '/gege', query= { 'player_id': 'student1' })
  except PlayoffException as e:
    assert 'route does not exist' in e.message

  players = pl.api(method = 'GET', route = '/players', query = { 'player_id': 'student1', 'limit': 1 })
  assert players['data'] != None
  assert players['data'][0] != None

  try:
    pl.get(route = '/player')
  except PlayoffException as e:
    assert "The 'player_id' parameter should be specified in the query" in e.message

  player_id = 'student1'
  player = pl.get(route = '/player', query = { 'player_id': player_id } )
  assert player["id"] == "student1"
  assert player["alias"] == "Student1"
  assert player["enabled"] == True

  pl.get(route = '/definitions/processes', query = { 'player_id': player_id } )
  pl.get(route ='/definitions/teams', query = { 'player_id': player_id } )
  pl.get(route = '/processes', query = { 'player_id': player_id } )
  pl.get(route = '/teams', query = { 'player_id': player_id } )

  processes = pl.get(route = '/processes', query = { 'player_id': 'student1', 'limit': 1, 'skip': 4 })
  assert processes["data"][0]["definition"] == "module1"
  assert len(processes["data"]), 1

  new_process = pl.post(route = '/definitions/processes/module1', query = { 'player_id': player_id })
  assert new_process["definition"] == "module1"
  assert new_process["state"] == "ACTIVE"

  patched_process = pl.patch(
    route = "/processes/%s" %new_process['id'],
    query = { 'player_id': player_id },
    body = { 'name': 'patched_process', 'access': 'PUBLIC' }
  )

  assert patched_process['name'] == 'patched_process'
  assert patched_process['access'] == 'PUBLIC'

  deleted_process = pl.delete(route = "/processes/%s" %new_process['id'], query = { 'player_id': player_id })
  assert deleted_process['message'] != None

  raw_data = pl.get(route = '/player', query = { 'player_id': player_id }, raw = True)
  assert type(raw_data) is str

def test_v2():
  pl = Playoff(
    version = 'v2',
    client_id=client_id,
    client_secret=client_secret,
    type = 'code'
  )

  try:
    pl.get(route= '/gege', query= { 'player_id': 'student1' })
  except PlayoffException as e:
    assert 'route does not exist' in e.message

  players = pl.api(method = 'GET', route = '/runtime/players', query = { 'player_id': 'student1', 'limit': 1 })
  assert players['data'] != None
  assert players['data'][0] != None

  try:
    pl.get(route = '/runtime/player')
  except PlayoffException as e:
    assert "The 'player_id' parameter should be specified in the query" in e.message

  player_id = 'student1'
  player = pl.get(route = '/runtime/player', query = { 'player_id': player_id } )
  assert player["id"] == "student1"
  assert player["alias"] == "Student1"
  assert player["enabled"] == True

  pl.get(route = '/runtime/definitions/processes', query = { 'player_id': player_id } )
  pl.get(route ='/runtime/definitions/teams', query = { 'player_id': player_id } )
  pl.get(route = '/runtime/processes', query = { 'player_id': player_id } )
  pl.get(route = '/runtime/teams', query = { 'player_id': player_id } )

  processes = pl.get(route = '/runtime/processes', query = { 'player_id': 'student1', 'limit': 1, 'skip': 4 })
  assert processes["data"][0]["definition"] == "module1"
  assert len(processes["data"]), 1

  new_process = pl.post(route = '/runtime/processes', query = { 'player_id': player_id }, body = { 'definition': 'module1' })
  assert new_process["definition"]['id'] == "module1"
  assert new_process["state"] == "ACTIVE"

  patched_process = pl.patch(
    route = "/runtime/processes/%s" %new_process['id'],
    query = { 'player_id': player_id },
    body = { 'name': 'patched_process', 'access': 'PUBLIC' }
  )

  assert patched_process['name'] == 'patched_process'
  assert patched_process['access'] == 'PUBLIC'

  deleted_process = pl.delete(route = "/runtime/processes/%s" %new_process['id'], query = { 'player_id': player_id })
  assert deleted_process['message'] != None

  raw_data = pl.get(route = '/runtime/player', query = { 'player_id': player_id }, raw = True)
  assert type(raw_data) is str


def store(access_token):
  print('Storing')
  print(access_token)

def test_store():
  pl = Playoff(
    version = 'v1',
    client_id=client_id,
    client_secret=client_secret,
    type = 'client',
    store = store
  )

def test_jwt():
  token = Playoff.createJWT(
    client_id=client_id,
    client_secret=client_secret,
    player_id='fbatista@deloitte.pt'
  )
  print("token-> " )
  print(str(token))

def test_auth():
  try:
    pl = Playoff(
      version = 'v1',
      client_id=client_id,
      client_secret=client_secret,
      type = 'code'
    )
  except PlayoffException as e:
    assert e.name == 'init_failed'

  pl = Playoff(
    version = 'v1',
    client_id=client_id,
    client_secret=client_secret,
    type = 'code',
    redirect_uri = 'https://localhost:3000/auth/callback'
  )
  print(str(pl.get_login_url()))

def get_player(player_id):
    
  return player

def get_all_players():
  pl = Playoff(
    client_id=client_id,
    client_secret=client_secret,
    type='client'
    ,allow_unsecure=True
  )
  players = pl.get(
      route='/admin/players',
      query={}
  )
  return players

def get_action_template(action_id):
    pl = Playoff(
        client_id=client_id,
        client_secret=client_secret,
        type='client'
        ,allow_unsecure=True
        ,hostname='playoffgenerali.it'
    )
    action = pl.get(
        route='/design/versions/latest/actions/'+action_id,
        query={}
    )
    return action

def create_challenge(challenge_id):
    pl = Playoff(
        client_id=client_id,
        client_secret=client_secret,
        type='client'
    )
    challenge_template_id =  'challenge_template'
    action = get_action_template(challenge_template_id)
    action['id'] = challenge_id
    action['name'] = 'ch1_gen'
    action['rules'][0]['rewards'][0]['value'] = "110"
    action['rules'][0]['rewards'][1]['value'] = "120"
    action['rules'][0]['rewards'][2]['value'] = "130"
    action['rules'][1]['rewards'][0]['value'] = "0"
    action['rules'][1]['rewards'][1]['value'] = "0"
    action['rules'][1]['rewards'][2]['value'] = "0"

    action = pl.post(
        route='/design/versions/latest/actions',
        body =action
    )
    return action

def update_challenge(challenge_id):
    pl = Playoff(
        client_id=client_id,
        client_secret=client_secret,
        type='client'
    )
    challenge_template_id =  'challenge_template'
    action = get_action_template(challenge_id)
    action.pop('id', None)#there cannot be an id for PATCH
    action['name'] = 'ch1_mod'
    action['rules'][0]['rewards'][0]['value'] = "1100"
    action['rules'][0]['rewards'][1]['value'] = "1200"
    action['rules'][0]['rewards'][2]['value'] = "1300"
    action['rules'][1]['rewards'][0]['value'] = "0"
    action['rules'][1]['rewards'][1]['value'] = "0"
    action['rules'][1]['rewards'][2]['value'] = "0"

    action = pl.patch(
        route = '/design/versions/latest/actions/'+challenge_id,
        body = action
    )
    return action

def delete_challenge(challenge_id):
    pl = Playoff(
        client_id=client_id,
        client_secret=client_secret,
        type='client'
    )
    challenge_template_id =  'challenge_tmp_max_01'
    action = get_action_template(challenge_template_id)
    action['id'] = challenge_id


    action = pl.delete(
        route='/design/versions/latest/actions/'+challenge_id
    )
    return action


test_jwt()


#

#print(get_player('supa'))
#print(get_all_players())
print (get_action_template('challenge_tmp_max_01'))
#ch print("ok")
#print(delete_challenge('sfida1'))
#print(create_challenge('sfida1'))
#print(update_challenge('sfida1'))

