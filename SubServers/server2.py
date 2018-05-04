#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2018 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

import sys
import Ice
import IceStorm

Ice.loadSlice('../META/server.ice')
import mp3App


class ServerI(mp3App.Function):

    songs = "sub2"
    def playMusic(self, music, current=None):
        print(self.songs)


def run(communicator):

    batch = False
    option = "Twoway"
    topicName = "mp3App"
    id = "2"
    retryCount = "1"

    if batch and (option in ("Twoway", "Ordered")):
        print("batch can only be set with oneway or datagram")
        sys.exit(1)

    manager = IceStorm.TopicManagerPrx.checkedCast(communicator.propertyToProxy('TopicManager.Proxy'))
    if not manager:
        print(" invalid proxy")
        sys.exit(1)

    #
    # Retrieve the topic.
    #
    try:
        topic = manager.retrieve(topicName)
    except IceStorm.NoSuchTopic as e:
        try:
            topic = manager.create(topicName)
        except IceStorm.TopicExists as ex:
            print("temporary error. try again")
            sys.exit(1)

    adapter = communicator.createObjectAdapter("mp3App.Subscriber")

    #
    # Add a servant for the Ice object. If --id is used the identity
    # comes from the command line, otherwise a UUID is used.
    #
    # id is not directly altered since it is used below to detect
    # whether subscribeAndGetPublisher can raise AlreadySubscribed.
    #

    subId = Ice.Identity()
    subId.name = id
    if len(subId.name) == 0:
        subId.name = Ice.generateUUID()
    subscriber = adapter.add(ServerI(), subId)

    #
    # Activate the object adapter before subscribing.
    #
    adapter.activate()

    qos = {}
    if len(retryCount) > 0:
        qos["retryCount"] = retryCount

    try:
        topic.subscribeAndGetPublisher(qos, subscriber)
    except IceStorm.AlreadySubscribed as ex:
        # If we're manually setting the subscriber id ignore.
        if len(id) == 0:
            raise
        print("reactivating persistent subscriber")

    communicator.waitForShutdown()

    #
    # Unsubscribe all subscribed objects.
    #
    topic.unsubscribe(subscriber)


#
# Ice.initialize returns an initialized Ice communicator,
# the communicator is destroyed once it goes out of scope.
#
with Ice.initialize(sys.argv, "../META/config.sub") as communicator:
    status = run(communicator)
