"""
Python Class Custom Data Model
"""
import json

class Settings():
    webhooks = ""
    anticaptcha_key = ""

    def to_json(self):
        data = {
            'webhooks': self.webhooks,
            'anticaptcha_key': self.anticaptcha_key
        }
        return json.dumps(data)
        
    def from_json(self, data_json):
        return json.loads(data_json)
    
    def set_settings(self, data):
        for key, value in data.items():
            exec('self.%s = "%s" ' %(key,value))
