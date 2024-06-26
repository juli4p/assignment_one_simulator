import requests, random

# data for cpee model
base_url = "https://cpee.org/flow/start/url/"
init_data = {
    "behavior": "fork_running",
    "url": "https://cpee.org/hub/server/Teaching.dir/Prak.dir/Challengers.dir/Julian_Simon.dir/Main.xml",
}
patient_type = "B1"
possible_patient_types = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"]

# amount of patients
num_requests = 25
# initial arrival time and increase per patient in hours
arrival_time = 8
increase_arrival_time = 0.5

# check whether time in hours lies between 8 and 17 and is a weekday
is_working_hour = lambda h: 0 <= (h // 24) % 7 < 5 and 8 <= h % 24 < 17

for i in range(num_requests):
    # random.random() = unif(0,1)
    increase_arrival_time = random.random()
    arrival_time = round(arrival_time + increase_arrival_time, 2)
    while not is_working_hour(arrival_time):
        #make sure the hospital is open
        arrival_time += 1
        
    patient_type = random.choice(possible_patient_types)
    # data for cpee model
    data = {
        **init_data,
        "init": f'{{"patient_type":"{patient_type}","arrival_time":"{arrival_time}"}}',
    }

    # create instance and print CPEE-INSTANCE
    try:
        response = requests.post(base_url, data=data)
        print(f"Request {i+1} - Status Code:", response.status_code)
        response_json = response.json()
        print(f"Request {i+1} - CPEE-INSTANCE:", response_json.get("CPEE-INSTANCE"))
    except Exception as e:
        print(f"Error in request {i+1}: {e}")
