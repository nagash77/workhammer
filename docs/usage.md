# API Usage

The API is designed to be used dynamically, this means that the only route that is
hard coded is the app root.  A GET to this route will return an object with defined
entrypoints for various parts of the application (these routes can change between
versions of the application).

## Requests

The system is designed to format the response data based on the 'Accept' HTTP
header, which should dictate the format of the response.  Right now the only
mimetypes handled are JSON and HTML.  The 'Content-Type' HTTP header is used to
dictate the format that the request data is in, the normal
'application/x-www-form-encoded' or 'application/json' are both used.  The JSON
mimetype is used mostly for creating complex models (like [Players](players.md) and
[Quests](quests.md)), the normal string with the "=" and "&" is used for requests
with a known set of arguments (Ideally, this would be adaptable, sometime).

## Example interaction

1. The user makes a GET request to '/' with 'Accept: application/json', then parses
the response body with their JSON parser of choice
1. The user uses the route hash table to make a POST request to the
route['register'] URL with the desired username and password, when the response
comes back with a 201, the user has been registered and logged in.
1. A GET request is made to route['players'] to see if the list of available
players
1. Upon noticing they have no player, a POST request to route['players'] is made
with a JSON encoded data string describing the player the user wants to make, when
the response comes back with a 201, the player has been made
1. Now that the user has a player, they are ready to log out, they send a GET
request to route['logout'] and move on with life.
