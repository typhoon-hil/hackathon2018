# Python hackathon
This document contains instructions to set up the hackathon environment, and an explanation of the hackathon task. Please, read it carefully and follow the instructions. 

# 1. Setup environment
In this section you will use Docker which is nessecery for running the hackathon project. Docker is a platform designed to help developers build, share, and run modern applications.

## 1.1. Install Docker
Install Docker if you don't have it already.

Docker installation can be found on https://www.docker.com/products/docker-desktop/

If you have Windows, you will need to install Windows Subsystem for Linux by following these instructions https://learn.microsoft.com/en-us/windows/wsl/install

If you are running an older build of Windows, you will maybe need to follow these instructions https://learn.microsoft.com/en-us/windows/wsl/install-manual

Open the Docker Desktop and check if the Docker Engine is running. If Docker Engine is running you should see a green tab like in the picture below. Otherwise, it will be red and in this case, you should restart your machine, and try again.

![image](https://user-images.githubusercontent.com/118435788/202661114-42f53673-4b20-4790-a340-930108c8b512.png)

## 1.2. Clone the hackathon project
Open the power shell and clone this project with the next command:

``` shell
git clone https://github.com/typhoon-hil/hackathon2022.git
```

## 1.3. Create solution directory
Create directory for solution (if you want to use different directory you need to modify docker run command later).
If you are on Windows:
``` shell
md c:\hackathon2022
```

If you are on Linux or Mac:
``` shell
mkdir home/you_user_name/hackathon2022
```
Unpack solution *hackathon_solution.tar* from cloned project directory to the solution directory *hackathon2022* you just made. This directory will be mounted as volume when you start docker container.

Download image from https://github.com/typhoon-hil/hackathon2022/releases/download/test_release2/uegos-docker-image.tar then open power shell in a directory where the image is downloaded. Load it in Docker and start it. To load the image and start it, follow these commands.
If you are on Windows:
``` shell
docker load --input uegos-docker-image.tar
docker run -e MONGO_INITDB_ROOT_USERNAME=uegos -e MONGO_INITDB_ROOT_PASSWORD=uegos -e MONGO_INITDB_DATABASE=uegos --name uegos-db -d mongo
docker run --link uegos-db -p 8080:8080 -v c:/hackathon2022:/app/gateway/plugins/hackathon_solution --name uegos -d uegos
```

If you are on Linux or Mac:
``` shell
docker load --input uegos-docker-image.tar
docker run -e MONGO_INITDB_ROOT_USERNAME=uegos -e MONGO_INITDB_ROOT_PASSWORD=uegos -e MONGO_INITDB_DATABASE=uegos --name uegos-db -d mongo
docker run --link uegos-db -p 8080:8080 -v home/you_user_name/hackathon2022:/app/gateway/plugins/hackathon_solution --name uegos -d uegos
```

# 2. Hackathon task 
The UEGOS is an operating system which is designed to allow aggregators, distribution system operators (DSOs), balance responsible parties (BRPs), virtual power plant (VPP) operations, and building architecture, engineering, construction, owner and operation (AECOO) entities and homeowners to install it on existing or new gateways. That way, UEGOS represents a communication solution that enables DSOs, BRPs, VPPs and other parties to quickly start monitoring and controlling their smart energy devices and appliances regardless of the communication protocol they are using, thus enabling them to utilize the flexibility of these devices and appliances to create new revenue streams, reduce CAPEX and OPEX and/or defer costly grid upgrades.


## 2.1 UEGOS - Universal Energy Gateway Operating System
Open http://localhost:8080/signin and login with credential (username: admin, password: 12345678). Then navigate to hackathon page (http://localhost:8080/hackathon) to see visualization of 7 days energy consumption. You can run simulation of your solution several times using the GUI button - **Restart** button at the bottom left corner. Each time, values will be slightly changed due to some random parameters like irradiance, blackouts and 'working from home' day.

Each time you modify solution you should **restart UEGOS docker container** (with stop and play buttons in Docker Desktop) for changes to take effect. 

## 2.2 Hackathon framework
The Hackathon framework is simulating energy consumption in a house during 7 days period. The framework is emitting data to the solution for each hour. The solution needs to decide how devices will behave in the following hour. The loads can be 'on' and 'off' and the car battery can be in 'charge', 'use', or 'idle' mode.

House can be supplied by the grid, pv panel, or by battery. House have two loads, further in text Load1 and Load2.
The user goes to work Monday through Friday and stays at home for the weekend. There is a 10% chance that the user will work from home each of the 5 workdays. If the user goes to work, the car battery is drained 45% and loads are turned off from 9h to 17h. The user expects loads to be powered on at certain times throughout the day, if they are not, penalties are rewarded. Load1 is expected to be used on the workday: from 7h - 9h and 17h - 23h, and on the home day from 7h - 23h. Load2 is expected to be used on a workday from 6h - 9h and 19h - 23h, and on the home day from 9h - 22h. 
If the user has to go to work but the car battery is under 50% he is forced to stay at home and car penalties are applied. Note: car penalties are not applied if the user decides to stay at home by himself that day.
PV power is random each day depending on the weather. Blackouts are random throughout the week.

The electricity price is cheap from 23h to 7h, and it has a value of 2$. Otherwise, it has an expensive tariff, which value is 7$. The selling (feed-in) price is better from 13h to 15h and has a value of 5$. Otherwise, it is low, and it has a price of 2$.

Input data are stored in *systemData* and they are:
 'car_plugged' : 0 or 1,
 'car_battery_SOC': in range [0.0, 100.0]%,
 'blackout': 0 or 1,
 'expected_load1',
 'expected_load2', 
 'actual_load1',
 'actual_load2',
 'electricity_price': 2$ or 7$,
 'feed_in_price': 2$ or 5$,
 'car_load',
 'grid_intake',
 'load1_penalty': 45$,
 'load2_penalty': 105$,
 'car_penalty': 1600$,
 'pv_power'.
  
 Data values that omitted can be read from diagrams on the hackathon board.


## 2.3 Your solution
The task for participants is to design a control system in that way the cost of the smart energy management house is minimized.
From the *hackathon2022* folder open *hackathon_solution.py* in the code editor you prefer. Your solution should be written in function *def uegos_send_data(systemData)*. You need to set output data which are stored in response. 


**Before you start working on your solution consider the proposed
solution architecture.**

**Proposed solution as well as framework requires Python 3.**

