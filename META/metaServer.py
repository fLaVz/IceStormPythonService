import sys
import Ice
import IceStorm
import time
import json

Ice.loadSlice('server.ice')
import mp3App


class ServerI(mp3App.Function):


    def playMusic(self, data, current=None):
        #print(data['action'])
        #print(data['song'])
        with Ice.initialize(sys.argv, "config.pub") as communicator:
            status = ServerI.run(communicator)

    def receivePlaylist(self, current=None):
        pl = ["test1", "test2"]
        return pl

    def run(communicator):
        topicName = "mp3App"

        manager = IceStorm.TopicManagerPrx.checkedCast(communicator.propertyToProxy('TopicManager.Proxy'))
        if not manager:
            print("invalid proxy")
            sys.exit(1)

        #
        # Retrieve the topic.
        #
        try:
            topic = manager.retrieve(topicName)
        except IceStorm.NoSuchTopic:
            try:
                topic = manager.create(topicName)
            except IceStorm.TopicExists:
                print("temporary error. try again")
                sys.exit(1)

        #
        # Get the topic's publisher object, and create a Clock proxy with
        # the mode specified as an argument of this application.
        #
        publisher = topic.getPublisher()
        publisher = publisher.ice_twoway()
        mp3 = mp3App.FunctionPrx.uncheckedCast(publisher)

        try:
            mp3.playMusic("hello")
            time.sleep(1)
        except IOError:
            pass
        except Ice.CommunicatorDestroyedException:
            pass

# Ice.initialize returns an initialized Ice communicator,
# the communicator is destroyed once it goes out of scope.

# Launch icebox service
# icebox --Ice.Config=config.icebox


with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("Function", "tcp -h 127.0.0.1 -p 4061")
    object = ServerI()
    adapter.add(object, communicator.stringToIdentity("server"))
    adapter.activate()
    communicator.waitForShutdown()
