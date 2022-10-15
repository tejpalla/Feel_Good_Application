from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
import random
from pathlib import Path
from datetime import datetime

Builder.load_file('draft.kv')
 
class LoginScreen(Screen):
    def signUp(self):
        print("signup button pressed")
        self.manager.current = "sign_up_screen"
    
    def go_to_loginSuccess(self, uname, pwd):
        print(uname, pwd)
        with open("users.json") as file:
            users = json.load(file)
        
        if uname in users and users[uname]["password"] == pwd:
            self.manager.current = "login_success_screen"
        else:
            self.ids.login_fail.text = "Wrong username or password"

class LoginSuccessScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def expression(self, feel):
        print(feel)
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings] 
        

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
                print(quotes)
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Feel something else :p"

class SignUpScreen(Screen):
    def add_user(self, uname, pwd):
        print(uname, pwd)
        with open("users.json") as file:
            users = json.load(file)
        
        users[uname] = {'username': uname, 'password': pwd,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json",'w') as file:
            json.dump(users,file)
        print(users)

        self.manager.current = "sign_up_success_screen"
    
class SignUpSuccessScreen(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()






