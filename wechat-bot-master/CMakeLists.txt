cmake_minimum_required(VERSION 3.20)
project(wechat_bot_master)

set(CMAKE_CXX_STANDARD 14)

include_directories(bin/GeneratedFiles)
include_directories(bin/GeneratedFiles/Debug)
include_directories(client/qt_c++)

add_executable(wechat_bot_master
        bin/GeneratedFiles/Debug/moc_addreg.cpp
        bin/GeneratedFiles/Debug/moc_friendaddreg.cpp
        bin/GeneratedFiles/Debug/moc_mask.cpp
        bin/GeneratedFiles/Debug/moc_predefs.h
        bin/GeneratedFiles/Debug/moc_wechatbot.cpp
        bin/GeneratedFiles/qrc_wechatbot.cpp
        bin/GeneratedFiles/ui_addreg.h
        bin/GeneratedFiles/ui_friendaddreg.h
        bin/GeneratedFiles/ui_mask.h
        bin/GeneratedFiles/ui_wechatbot.h
        client/qt_c++/addreg.cpp
        client/qt_c++/addreg.h
        client/qt_c++/cJSON.c
        client/qt_c++/cJSON.h
        client/qt_c++/friendaddreg.cpp
        client/qt_c++/friendaddreg.h
        client/qt_c++/logic.cpp
        client/qt_c++/logic.h
        client/qt_c++/main.cpp
        client/qt_c++/mask.cpp
        client/qt_c++/mask.h
        client/qt_c++/tools.cpp
        client/qt_c++/tools.h
        client/qt_c++/wechatbot.cpp
        client/qt_c++/wechatbot.h)
