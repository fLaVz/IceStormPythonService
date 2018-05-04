// **********************************************************************
//
// Copyright (c) 2003-2017 ZeroC, Inc. All rights reserved.
//
// **********************************************************************

#pragma once

module mp3App
{

    struct Song
    {
        string name;
        string artist;
        string genre;
        string length;
        string path;
    };

    sequence<string> playList;

    interface Function
    {
        void sendPlayList(playList seq);
        void add(Song son);
        void remove(string name);
        void searchByName(string name);
        void searchByGenre(string genre);
        void searchByArtist(string name);
        void printPlayList();
        playList receivePlaylist();
        void playMusic(string music);
        void stopMusic();
    };
};