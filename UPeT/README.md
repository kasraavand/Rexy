## Preamble

This application is supposed to receive the data from a remote server through an API and prepare them in order to be sent to the data analyzer system. Then extract the analyzed data and send back the analyzed result to the server.

`UPeT` has been designed upon a high abstraction level. It's composed of three major entities which are the basis on any social and commercial application. These entities are `User`, `Product` and `Tag`.

### Implementation details


`UPeT` has been written in python language and it used following technologies:

  - Python 3.4+<sup>1</sup>
  - [Aerospike](https://github.com/aerospike)(As the database engine)
  - [Requests](https://github.com/kennethreitz/requests)(Python HTTP Requests for Humans)


`UPeT` is contain following modules which all of them can be overridden based on custom needs.

  - Importer
    - import raw data and analyzed data to database 
  - Exporter
    - export raw and analyzed data from database
  
![image](https://cloud.githubusercontent.com/assets/5694520/23091073/a2732524-f5c2-11e6-927a-13d6bb2bfbce.png)
  - Middleware
    - contain middleware modules for sake of customizing the data befor and after interacting with database.
  - Transmission
    - contains `sender` and `receiver` modules for interacting with server. 

------
<sub>
1. If you are lookig for the older versions support you might find it in the rivers. 
</sub>
