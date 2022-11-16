# Python hackathon
This document contains instructions to setup hackathon environment, and explanation of hackathon task.

# Setup environment
Firstly, clone this project:

``` shell
git clone https://github.com/typhoon-hil/hackathon2022.git
```

## Install Docker
Install docker if you don't have it already.

Docker installation can be found on https://www.docker.com/products/docker-desktop/

If you have Windows, you will need to install Windows Subsystem for Linux by following these instructions https://learn.microsoft.com/en-us/windows/wsl/install

If you are running an older build of Windows, you will maybe need to follow these instruction https://learn.microsoft.com/en-us/windows/wsl/install-manual

## Create solution directory
Create directory for solution (if you want to use different directory you need to modify docker run command later)
``` shell
md c:\hackathon2022
```
Unpack solution from this repo hackathon_solution.tar to solution directory. This directory will be mounted as volume when you start docker container.

Download image from https://github.com/typhoon-hil/hackathon2022/releases/download/test_release/uegos-docker-image.tar, load it in docker and start it:
``` shell
docker load --input uegos-docker-image.tar
docker run -e MONGO_INITDB_ROOT_USERNAME=uegos -e MONGO_INITDB_ROOT_PASSWORD=uegos -e MONGO_INITDB_DATABASE=uegos --name uegos-db -d mongo
docker run --link uegos-db -p 8080:8080 -v c:/hackathon2022:/app/gateway/plugins/hackathon_solution --name uegos -d uegos
```

# UEGOS
Open localhost:8080/hackathon to see visualization of 7 days energy consumption. You can run simulation of your solution several times using the GUI button - Restart button at the bottom left corner. Each time, values will be slightly changed due to some random parameters like irradiance, blackouts and 'working from home' day.

Each time you modify solution you should restart UEGOS docker container (with stop and play buttons in Docker Desktop) for changes to take effect. 

**Before you start working on your solution consider the proposed
solution architecture.**

**Proposed solution as well as framework requires Python 3.**

## Hackathon framework
Hackathon framework is simulating energy consumption in a house during 7 days period. Framework is emitting data to solution for each hour. The solution needs to decide how devices will behave in the following hour. The loads can be 'on' and 'off' and car battery can be in 'charge', 'use' or 'idle' mode.

The user goes to work Monday through Friday and stays at home for weekend. There is 10% chance user will work from home each of 5 workdays. If user goes to work, car battery is drained 45% and loads are turned off from 9h to 17h. User expects loads to be powered on at certain times through out the day, if they are not, penalties are rewarded. Load1 is expected to be used on workday: from 7h - 9h and from 17h - 23h. Load1 on homeday: from 7h - 23h. Load2 on workday: from 6h - 9h and from 19h - 23h. Load2 on homeday: from 9h - 22h. If user has to go to work but car battery is under 50% he is forced to stay at home and car penalties are applied. Note: car penalties are not applied if user decides to stay at home by himself that day.

PV power is random each day depending on weather. Blackouts are random throughout the week.

Electricity price is cheap (2) from 23h to 7h. Otherwise its expensive tariff (7).
Selling (feed in) price is better (5) from 13h to 15h, otherwise its low (2).
