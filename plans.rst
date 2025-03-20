1) [+] typecast url params to controller handler. inspect funct according to type annotations

2) [+] error handling -> http_status set by rest

3) [+] parsing of request body according to content-type, and put it into handler according to param. (like fastAPI)

4) simple-like DI shit

5) better headers propagation. now like shit, no headers in response...

6) [+] fix routing -> app registration


! add ws handling
7) add configs like: parse confs on startup, add mdlwrs, exclusions register for mdlwars
8) add skip mdlwr(s) decorator for Handler and method
9) add lifespan method registration

