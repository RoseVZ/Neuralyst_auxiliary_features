from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv
import re
from pydub import AudioSegment
import io
from io import BytesIO
import json
from datetime import datetime


# Load environment variables
load_dotenv()
# Initialize Flask app
app = Flask(__name__)
# Get Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

headers = {
    'Authorization': f'Bearer {GROQ_API_KEY}',
    'Content-Type': 'application/json'
}
# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
@app.route('/algo', methods=['POST'])
def algo():
#     #Case1
    data = request.get_json()
    cur_task_list = data.get('task_list')
# Get current date and time
    now = datetime.now()
    current_date = now.date()
    print("Current Date:", current_date)
    current_time = now.time()
    print("Current Time:", current_time)
    #get a json of task_id: task
    # task = {
    #     "1": "Go to the gym",
    #     "2": "Cook food",
    #     "3": "Complete project report in the evening",
    #     "4": "Attend meeting at 10pm",
    #     "5": "Go for a run",
    # }
    # Convert dictionary to string
    task_string = json.dumps(cur_task_list)
    completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                    "role": "user",
        "content": f"""I have a list of tasks that have the following format, <task_id> : "task".  Can you help me get <task id>: prority_number by chronologically sorting them. The criterion for sorting are-if the task implies today, then consider it to be done today atleast 15 mins before the time mentioned. The actual time now is {current_time} if the task has a date, the current date should be compared to. The actual date is {current_date} and then the task is prioritized in accordance with others.
        Generic tasks like "Go to the gym" or "cook food" should be today at approprite times taking into consideration the current time. 
        The task list is as follows
    The tasks are {task_string}
    Just give a chronological sort and return in the form of <task_id>,<task_name>,<Priority><task time><endtime> dont return anything else The end time can be approximated by you. 
    prority 1 means it is the most important and now mean most priority, And please make sure the the task_ids are consistent with the input task_ids
        """
                    }
                ],
                temperature=0.7,
                max_completion_tokens=500
                ,
                top_p=0.95,
                stream=True,
                
            )
    priority = ""
    for chunk in completion:
        priority += chunk.choices[0].delta.content or ""
    print(priority)
    # Split into lines and process each line
    tasks = []
    for line in priority.split("\n"):
        task_id, task_name, priority_val, start_time, end_time = line.split(",")
        tasks.append({
            "task_id": int(task_id),
            "task_name": task_name,
            "priority": int(priority_val),
            "start_time": start_time,
            "end_time": end_time
        })

    # Convert to JSON
    # tasks_json = json.dumps(tasks, indent=4)

    # print(tasks_json)
    return jsonify(tasks)
if __name__ == '__main__':
    app.run(debug=True)
