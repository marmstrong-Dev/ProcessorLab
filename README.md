Processor Lab
======

*Version: 0.1*

---

### Overview

Data for storing information regarding various CPU and GPU models. This will be protected using JWT authentication for user accounts.

This will be used for lab testing with Python and MongoDB.

---

### Tech Stack

- Python 3.11
- Flask
- MongoDB
- Docker
- Swagger for API Documentation

---

### Endpoints
<br/>

*Misc*

- ```/api/status``` - GET - Returns the status of the API

*Accounts*

- ```/api/auth/register``` - POST - Registers a new account
- ```/api/auth/login``` - POST - Generates a JWT token for the user
- ```/api/auth/refresh``` - POST - Refreshes the JWT token for the user
- ```/api/auth/update``` - PUT - Updates the user's account information
- ```/api/auth/status``` - PUT - Activate / Deactivate the user's account

*Central Processors*

*Graphics Processors*
