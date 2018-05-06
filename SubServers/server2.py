#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2018 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

import sys
import Ice
import IceStorm
from os import listdir
from os.path import isfile, join

Ice.loadSlice('../META/server.ice')
import mp3App
import vlc


class ServerI(mp3App.Function):

    playList = ["test2.mp3"]
    instance = vlc.Instance()
    player = instance.media_player_new()

    def sendPlayList(self, seq, current=None):
        self.playList = seq

    def receivePlaylist(self, current=None):
        self.playList = [f for f in listdir("S2Playlist/") if isfile(join("S2Playlist/", f))]
        print("Musics on server : ")
        print(self.playList)
        return self.playList

    def add(self, son, current=None):
        if not self.searchByName(son.name):
            self.playList.append(son)
            print("'" + son.name + "' added to playList")

    def remove(self, name, current=None):
        for aSong in self.playList:
            if aSong.name == name:
                self.playList.remove(aSong)
                print("'" + aSong.name + "' removed from playList\n")

    def searchByName(self, name, current=None):
        for aSong in self.playList:
            if aSong.name == name:
                print("Music '" + aSong.name + "' found in playList \n")
                return True
        return False

    def searchByGenre(self, genre, current=None):
        print("Genre '" + genre + "':")
        for aSong in self.playList:
            if aSong.genre == genre:
                print("Music '" + aSong.name + "'")
        print("\n")

    def searchByArtist(self, artist, current=None):
        print("Artist '" + artist + "':")
        for aSong in self.playList:
            if aSong.artist == artist:
                print("Music '" + aSong.name + "'")
        print("\n")

    def printPlayList(self, current=None):
        print("PlayList: ")

        for aSong in self.playList:
            print(aSong.name + " || " + aSong.artist + " || " + aSong.genre + " || " + aSong.length + " || " + aSong.path)
        print("\n")

    def playMusic(self, music, current=None):
        if self.player is None and self.instance is None:
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()

        if self.playList.__contains__(music):
            options = ':sout=#transcode{vcodec=none,acodec=mp3,ab=128,channels=2,samplerate=44100}:http{mux=mp3,dst=:8080/player.mp3}'
            media = self.instance.media_new('/S2Playlist/' + music, options)
            print("playing music : " + music)
            self.player.set_media(media)
            self.player.play()
        else:
            print("music not available on server")

    def stopMusic(self, current=None):
        if self.player is not None:
            print("stoping music")
            self.player.stop()
            self.player.release()
            self.instance = None
            self.player = None
            # http://localhost:8080


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
