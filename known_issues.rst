
Routing
----

* Incorrect routing building with tree

    @r.route('/test1') and @r.route('/test2') -> splits by common 'test' and 1 and 2 go separate

* Potentially sensitive info returns to client while raising exception

* No ability to close WS connection from endpoint side

* No multipart data support