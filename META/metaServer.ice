// **********************************************************************
//
// Copyright (c) 2003-2017 ZeroC, Inc. All rights reserved.
//
// **********************************************************************

#pragma once

module metaServer
{
    sequence<string> playList;

    interface msFunction
    {
        void parse(string data, string action);
        playList receive();
    };
};