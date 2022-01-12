cmake_minimum_required(VERSION 3.20)
project(qt_c__)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)
include_directories(.idea)
include_directories(.vs)
INCLUDE(CMakeForceCompiler)
CMAKE_FORCE_C_COMPILER(gcc GNU)
CMAKE_FORCE_CXX_COMPILER(g++ GNU)


add_executable(qt_c__
        .idea/.gitignore
        .idea/modules.xml
        .idea/qt_c++.iml
        .idea/workspace.xml
        .vs/qt_c++/v16/ipch/AutoPCH/35dc867b7792f71/LIMITS.ipch
        .vs/qt_c++/v16/ipch/AutoPCH/7930e5675bfa1af/CJSON.ipch
        .vs/qt_c++/v16/ipch/AutoPCH/f9b038fea1eb2af7/TOOLS.ipch
        .vs/qt_c++/v16/Browse.VC.db
        .vs/ProjectSettings.json
        .vs/slnx.sqlite
        .vs/tasks.vs.json
        .vs/VSWorkspaceState.json
        .gitignore
        addreg.cpp
        addreg.h
        addreg.ui
        cJSON.c
        cJSON.h
        CppProperties.json
        friendaddreg.cpp
        friendaddreg.h
        friendaddreg.ui
        loading.gif
        logic.cpp
        logic.h
        main.cpp
        mask.cpp
        mask.h
        mask.ui
        README.md
        tools.cpp
        tools.h
        wechat.ini
        wechatbot.cpp
        wechatbot.h
        wechatbot.qrc
        WeChatBot.sln
        wechatbot.ui
        WeChatBot.vcxproj
        WeChatBot.vcxproj.filters
        WeChatBot.vcxproj.user)
