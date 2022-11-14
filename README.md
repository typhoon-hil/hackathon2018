# Python hackathon
This documents contains basic explanation of implementation part.

# Solve the challenge
Firstly, clone this project:

``` shell
git clone <path_to_this_repo>
```

# Docker
Install docker if you dont have it already. 
Create directory for solution (if you want to use different directory you need to modify file start-gateway.sh)
``` shell
mkdir C:/hackathon2022
```

Unpack solution from this repo hackathon_solution.tar to solution directory. 

Download image from this repo release binary, load it in docker and start it:
``` shell
docker load uegos-docker-image.tar
sh start-database.sh
sh start-gateway.sh
```

# UEGOS
Open localhost:8000/hackathon to see visualisation of 7 days energy consumption. You can run simulation of your solution several times using the GUI button. Each time, values will be slightly changed due to some random parameters like irradiance, blackouts and 'working from home' day.

Each time you modify solution you should restart uegos docker container for changes to take effect. 

**Before you start working on your solution consider the proposed
solution architecture.**

**Proposed solution as well as framework requires Python 3.**

## UEGOS framework
UEGOS framework is emitting data to solution for each hour. The solution needs to decide how devices will behave in the following our. The loads can be 'on' and 'off' and car battery can be in 'charge', 'use' or 'idle' mode.

