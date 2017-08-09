# jantjie
JSON Api Network Translator for Just Interacting Easily

## Idea

The job of a server-side web application can largely be delegated to the client
side, by serving content as JSON. The actual rendering of the content as HTML
can be performed by the client. Moreover, alternative clients (e.g. mobile
applications) can render the content in a completely different way.

What content does the server-side application need to serve?

1. Static content.
   Example request: /base.css

2. Dynamic web pages. The server serves the basic framework, as well as
   Javascript code to fetch the JSON-delivered content and render it
   appropriately.
   Example request: /thread/12345

3. Raw data. This is the content delivered in JSON format. It is stored in a
   database on the server.
   Example request: /api/thread/12345/posts

The first two jobs are relatively simple for a server; it needs only to deliver
some predetermined strings, perhaps with a couple of identifiers injected in
(for example, to give a thread id, or the date). This can be done with an
extremely simple templating system.

The latter is deceptively simple too! The server reacts to an api request by
making a corresponding call to a database system, parsing the result, encoding
it in JSON, and returning it. In the case of a forum, this is as simple as
translating between a GET request, SQL, database result, and JSON. The server
would need only a list of prepared statements and a grammar to match the GET
request against.
