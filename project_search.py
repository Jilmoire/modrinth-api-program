import json
import signal
import subprocess
import time
import requests

class NodeProcessManager: #Opens the API layer to connect to modrinth's API
    def __init__(self, node_path = None):
        self.api_path = node_path
        self.process = None
    
    def launchAPI(self):
        try:
            if self.api_path is None:
                with open("general_config.json", "r") as cfile:
                    config = json.load(cfile)
                    self.api_path = config["node_api_path"]
                    
                    print(f"Starting API found in: {self.api_path}")
                    
                    if self.process is None:    
                        self.process = subprocess.Popen(["node", self.api_path])
                        print("API Started")
                    else:
                        print("Process is already running!")   
                    
                    return self.api_path         
        except FileNotFoundError:
            print("Config file not found!")
        
        except json.JSONDecodeError:
            print("Invalid JSON format!")
    
    def stopAPI(self):
        if self.process is not None:
            print("Terminating API layer...")
            self.process.send_signal(signal.SIGINT)
            self.process.wait()
            print("API process terminated.")
            self.process = None
        else:
            print("No process to stop.")
            
class ModrinthProjectSelector: #Waits for data retrieval before listing possible projects
    def __init__(self, projects_list=None):
        self.projects_list = projects_list if projects_list is not None else []
        self.total_hits = 0
        
    def received_data(self, data):
        if not data or not "hits" in data:
            print("No project related to your search was found.")
            return None
        
        self.projects_list = data["hits"]
        self.total_hits = data.get("total_hits", 0)
        print(f"Received {len(self.projects_list)} projects out of {self.total_hits} total hits.")

        index = 0
        for project in self.projects_list:
            index += 1
            title = project.get("title", "Unnamed")
            slug = project.get("slug", "Unknown")
            print(f"{index}. {title} (Slug: {slug})")

class APIDataRetriever: #Collects data after the API layer finished sending requests
    def __init__(self, api_url):
        self.data = None
        self.api_url = api_url
        
    def data_retriever(self):
        try: 
            if self.data is None:
                response = requests.get(self.api_url)
                response.raise_for_status()
                self.data = response.json()
            else:
                print(f"{self.data} contains data already!")
        except subprocess.CalledProcessError as e:
            print("Error running Node script:", e)
        except json.JSONDecodeError as e:
            print("Error decoding JSON from Node script:", e)

if __name__ == "__main__":
    manager = NodeProcessManager()
    manager.launchAPI()
    
    time.sleep(5)
    
    api_url = "http://localhost:3000/data"
    
    retriever = APIDataRetriever(api_url)
    retriever.data_retriever()
    
    selector = ModrinthProjectSelector()
    selector.received_data(retriever.data)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stopAPI()
