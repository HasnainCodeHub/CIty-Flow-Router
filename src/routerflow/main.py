from crewai.flow.flow import Flow,start,listen,router,or_
from litellm import completion
from dotenv import load_dotenv
import os,random

load_dotenv()
class RouteFlow(Flow):
    @start()
    def greeting(self):
        print("Hello, I'm an llm based application...")
        cities=['karachi','lahore','islamabad']
        select_city = random.choice(cities)
        self.state['city'] = select_city
        

    @router(greeting)   
    def city_name(self):  
        if self.state['city'] == 'karachi':
            print(f"City Selected: {self.state['city']}")
            return 'karachi'
        elif self.state['city'] == 'lahore':
            print(f"City Selected: {self.state['city']}")
            return 'lahore'
        else :
            return 'islamabad' 
            print(f"City Selected: {self.state['city']}")

    @listen('karachi')
    def f1(self):
        response = completion(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GEMINI_API_KEY"),
            messages=[{"role": "user", "content": f"Write a 100 words Description about {self.state['city']}"}])
        result = response.choices[0].message.content
        print(f"Description: {result}")
        return result


    @listen('lahore')
    def f2(self,city):
        response = completion(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GEMINI_API_KEY"),
            messages=[{"role": "user", "content": f"Write a 100 words Description about {self.state['city']}"}])
        result = response.choices[0].message.content
        print(f"Description: {result}")
        return result


    @listen('islamabad')
    def f3(self,city):
        response = completion(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GEMINI_API_KEY"),
            messages=[{"role": "user", "content": f"Write a 100 words Description about {self.state['city']}"}])
        result = response.choices[0].message.content
        print(f"Description: {result}")
        return result

    @listen(or_('f1','f2','f3'))   
    def save_to_file(self, result):
        with open(f"{self.state['city']}.md", "w") as file:
            file.write(result)
        print(f"Description saved to {self.state['city']}.md")



def kickoff():
    flow = RouteFlow()
    flow.kickoff()
    

def plot():
    flow = RouteFlow()
    flow.plot()   