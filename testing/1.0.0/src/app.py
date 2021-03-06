import socket
import asyncio
import time
import random
import json
import requests

from walkoff_app_sdk.app_base import AppBase

class HelloWorld(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "1.0.0"
    app_name = "hello_world"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def hello_world(self):
        """
        Returns Hello World from the hostname the action is run on
        :return: Hello World from your hostname
        """
        message = f"Hello World from {socket.gethostname()} in workflow {self.current_execution_id}!"

        # This logs to the docker logs
        self.logger.info(message)

        return message

    async def repeat_back_to_me(self, call):
        return call

    async def repeat_back_to_me_multi(self, call, call2, call3):
        return {"call1": call, "call2": call2, "call3": call3} 

    async def return_plus_one(self, number):
        return str(number + 1)

    async def pause(self, seconds):
        time.sleep(seconds)
        return "Waited %d seconds" % seconds

    async def get_type(self, value):
        return "Type: %s" % type(value)

    async def input_options_test(self, call):
        return "Value: %s" % call 

    async def get_file(self, filedata):
        if filedata == None:
            return "File is empty?"

        file_content = filedata
        return file_content 

    async def upload_file(self, filename, data):
        print("Inside function")
        filedata = {
            "filename": filename,
            "data": data,
        }
        print("Done with function")

        return ("Successfully put your data in a file", filedata)

    async def delete_file(self, file_id):
        headers = {
            "Authorization": "Bearer %s" % self.authorization,
        }
        print("HEADERS: %s" % headers)

        ret = requests.delete("%s/api/v1/files/%s?execution_id=%s" % (self.url, file_id, self.current_execution_id), headers=headers)
        return ret.text

if __name__ == "__main__":
    asyncio.run(HelloWorld.run(), debug=True)
