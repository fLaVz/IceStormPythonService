import sys
import Ice
import IceStorm
import time
import json

from os import listdir
from os.path import isfile, join

Ice.loadSlice('server.ice')
import mp3App
import metaServer


class MetaServerI(metaServer.msFunction):

    musicList = ["test1.mp3", "test2.mp3"]

    def __init__(self):
        print("init")


    def parse(self, data, action, current=None):
        #print(data['action'])
        #print(data['song'])
        print("parsing....  -> " + data)

        with Ice.initialize(sys.argv, "config.pub") as communicator:
            status = MetaServerI.run(self, communicator, action, data)

    def receive(self, current=None):
        return self.musicList

    def run(self, communicator, action, data):

        topicName = "mp3App"
        manager = IceStorm.TopicManagerPrx.checkedCast(communicator.propertyToProxy('TopicManager.Proxy'))
        if not manager:
            print("invalid proxy")
            sys.exit(1)

        # Retrieve the topic.
        try:
            topic = manager.retrieve(topicName)
        except IceStorm.NoSuchTopic:
            try:
                topic = manager.create(topicName)
            except IceStorm.TopicExists:
                print("temporary error. try again")
                sys.exit(1)

        # Get the topic's publisher object, and create a proxy
        publisher = topic.getPublisher()
        publisher = publisher.ice_twoway()
        mp3 = mp3App.FunctionPrx.uncheckedCast(publisher)

        # Handling actions
        try:
            if action == "init":
                print("init")
            elif action == "play":
                mp3.playMusic(data)
            elif action == "stop":
                mp3.stopMusic()

        except IOError:
            pass
        except Ice.CommunicatorDestroyedException:
            pass

# Ice.initialize returns an initialized Ice communicator,
# Launch icebox service
# icebox --Ice.Config=config.icebox
with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("Function", "tcp -h 127.0.0.1 -p 4061")
    object = MetaServerI()
    adapter.add(object, communicator.stringToIdentity("server"))
    adapter.activate()
    communicator.waitForShutdown()
