#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from config import module_configuration


def now(model="%b  %d, %Y %I:%M %p"):
    return datetime.datetime.now().strftime(model)


def I10100():
    return "".join(
        [
            '\x01\r\nI10100\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'SYSTEM STATUS REPORT',
            '\r\n\r\n',
            'D 8:ALARM CLEAR WARNING',
            '\r\n\r\n',
            '\x03'
        ]
    )


def I10200():
    return "".join(
        [
            '\x01\r\nI10200\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'SYSTEM CONFIGURATION',
            '\r\n\r\n',
            'SLOT  BOARD TYPE                    POWER ON RESET     CURRENT\r\n',
            '  1   PLLD SENSOR BD                     3882             3864\r\n',
            '  2   INTERSTITIAL BD                  202440           201698\r\n',
            '  3   8SMARTSENSOR BD                   39681            39594\r\n',
            '  4   4 PROBE / G.T.                   164489           164087\r\n',
            '  5   UNUSED                          9922452          9806112\r\n',
            '  6   UNUSED                          9895411          9794026\r\n',
            '  7   UNUSED                          9911016          9789239\r\n',
            '  8   UNUSED                          9892610          9806957\r\n',
            '  9   PLLD POWER BD                    100307           100205\r\n',
            ' 10   PLLD POWER BD                    100133            99984\r\n',
            ' 11   UNUSED                          9902247          9793640\r\n',
            ' 12   UNUSED                          9906330          9807243\r\n',
            ' 13   UNUSED                          9885509          9793619\r\n',
            ' 14   UNUSED                          9904257          9790045\r\n',
            ' 15   UNUSED                          9893889          9800940\r\n',
            ' 16   UNUSED                          9890811          9786016\r\n',
            '      COMM 1 ELEC DISP INT.            100852           100802\r\n',
            '      COMM 2 SERIAL SAT BD             481672           480551\r\n',
            '      COMM 3 UNUSED                   9906416          9803929\r\n',
            '      COMM 4 UNUSED                   9884056          9782746\r\n',
            '      COMM 5 UNUSED                   9898186          9806203\r\n',
            '      COMM 6 UNUSED                   9890469          9786623\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I11100():
    return "".join(
        [
            '\x01\r\nI11100\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'PRIORITY ALARM HISTORY\r\n',
            'ID  CATEGORY  DESCRIPTION          ALARM TYPE           STATE    DATE    TIME\r\n',
            'Q 4 OTHER     DIESEL               PERIODIC LINE FAIL   CLEAR   7-09-18  2:49PM\r\n',
            'Q 4 OTHER     DIESEL               PERIODIC LINE FAIL   ALARM   7-09-18  4:36AM\r\n',
            'Q 4 OTHER     DIESEL               PLLD SHUTDOWN ALARM  CLEAR   6-19-18  9:01AM\r\n',
            'Q 4 OTHER     DIESEL               GROSS LINE FAIL      CLEAR   6-19-18  9:01AM\r\n',
            'Q 4 OTHER     DIESEL               PLLD SHUTDOWN ALARM  ALARM   6-19-18  8:46AM\r\n',
            'Q 4 OTHER     DIESEL               GROSS LINE FAIL      ALARM   6-19-18  8:46AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   5-10-18 11:29AM\r\n',
            'Q 3 OTHER     SUPREME              GROSS LINE FAIL      CLEAR   5-10-18 11:29AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        CLEAR   5-10-18 11:24AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  ALARM   5-10-18 10:52AM\r\n',
            'Q 3 OTHER     SUPREME              GROSS LINE FAIL      ALARM   5-10-18 10:52AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        ALARM   5-10-18 10:43AM\r\n',
            'Q 4 OTHER     DIESEL               PLLD SHUTDOWN ALARM  CLEAR   4-19-18 11:34AM\r\n',
            'Q 4 OTHER     DIESEL               GROSS LINE FAIL      CLEAR   4-19-18 11:34AM\r\n',
            'Q 2 OTHER     PLUS                 PLLD SHUTDOWN ALARM  CLEAR   4-19-18 11:33AM\r\n',
            'Q 2 OTHER     PLUS                 GROSS LINE FAIL      CLEAR   4-19-18 11:33AM\r\n',
            'Q 1 OTHER     REGULAR              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 11:33AM\r\n',
            'Q 1 OTHER     REGULAR              GROSS LINE FAIL      CLEAR   4-19-18 11:33AM\r\n',
            'L 2 ANNULAR   PLUS ANNULAR         FUEL ALARM           CLEAR   4-19-18 11:09AM\r\n',
            'L 2 ANNULAR   PLUS ANNULAR         FUEL ALARM           ALARM   4-19-18 11:06AM\r\n',
            'L 1 ANNULAR   REGULAR ANNULAR      FUEL ALARM           CLEAR   4-19-18 11:01AM\r\n',
            'L 1 ANNULAR   REGULAR ANNULAR      FUEL ALARM           ALARM   4-19-18 11:00AM\r\n',
            'L 4 ANNULAR   DIESEL ANNULAR       FUEL ALARM           CLEAR   4-19-18 10:55AM\r\n',
            'L 4 ANNULAR   DIESEL ANNULAR       FUEL ALARM           ALARM   4-19-18 10:51AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        CLEAR   4-19-18 10:46AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        ALARM   4-19-18 10:45AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              WATER ALARM          CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              WATER ALARM          ALARM   4-19-18 10:45AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  ALARM   4-19-18 10:45AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              FUEL ALARM           CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              FUEL ALARM           ALARM   4-19-18 10:45AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  ALARM   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        ALARM   4-19-18 10:44AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:43AM\r\n',
            's 6 OTHER     3,4 PAN              WATER ALARM          CLEAR   4-19-18 10:43AM\r\n',
            's 6 OTHER     3,4 PAN              WATER ALARM          ALARM   4-19-18 10:42AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  ALARM   4-19-18 10:42AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:42AM\r\n',
            's 6 OTHER     3,4 PAN              FUEL ALARM           CLEAR   4-19-18 10:42AM\r\n',
            's 6 OTHER     3,4 PAN              FUEL ALARM           ALARM   4-19-18 10:42AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  ALARM   4-19-18 10:42AM\r\ns',
            ' 7 OTHER     5,6 PAN-DIESEL       WATER ALARM          CLEAR   4-19-18 10:41AM\r\n',
            's 7 OTHER     5,6 PAN-DIESEL       WATER ALARM          ALARM   4-19-18 10:41AM\r\n',
            's 7 OTHER     5,6 PAN-DIESEL       FUEL ALARM           CLEAR   4-19-18 10:41AM\r\n',
            's 7 OTHER     5,6 PAN-DIESEL       FUEL ALARM           ALARM   4-19-18 10:41AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:40AM\r\n',
            's 5 OTHER     1,2 PAN              WATER ALARM          CLEAR   4-19-18 10:40AM\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I11200():
    return "".join(
        [
            '\x01\r\nI11200\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'NON-PRIORITY ALARM HISTORY\r\n',
            'ID  CATEGORY  DESCRIPTION          ALARM TYPE           STATE    DATE    TIME\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      CLEAR   8-02-18  5:36AM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      ALARM   8-02-18  5:09AM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   7-24-18  4:17PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      ALARM   7-24-18  1:36PM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      CLEAR   6-29-18  5:40PM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      ALARM   6-29-18  2:58AM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   6-20-18 12:15AM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   6-19-18  6:29PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   6-14-18  3:11PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      ALARM   6-14-18  1:56PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   6-06-18  5:50PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   6-06-18  1:52PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   5-18-18  6:11AM\r\n',
            '    SYSTEM                         PAPER OUT            CLEAR   5-18-18  6:11AM\r\n',
            '    SYSTEM                         PRINTER ERROR        ALARM   5-18-18  6:10AM\r\n',
            '    SYSTEM                         PAPER OUT            ALARM   5-18-18  6:10AM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   5-15-18 10:03PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   5-15-18  9:58PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      ALARM   5-15-18  6:56PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   5-15-18  6:49PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   5-11-18  3:08PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   5-11-18  3:07PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      ALARM   5-11-18 12:07PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   5-10-18 10:52PM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      CLEAR   5-08-18  1:08PM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      ALARM   5-07-18  3:16PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-26-18 10:47PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   4-26-18 12:43PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-23-18  8:34PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   4-23-18  6:29PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   4-20-18  6:15PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      ALARM   4-20-18  5:50PM\r\n',
            's 1 OTHER     REGULAR STP SUMP     WATER WARNING        CLEAR   4-19-18 10:31AM\r\n',
            's 1 OTHER     REGULAR STP SUMP     WATER WARNING        ALARM   4-19-18 10:31AM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-14-18 11:34PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   4-14-18  2:39PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-10-18  9:03PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      ALARM   4-10-18 11:01AM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   4-04-18 12:33AM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      ALARM   4-03-18 11:06PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        ALARM   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PAPER OUT            CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        ALARM   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PAPER OUT            ALARM   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        ALARM   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PAPER OUT            CLEAR   3-30-18  9:58PM\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I11300():
    return "".join(
        [
            '\x01\r\nI11300\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'ACTIVE ALARMS REPORT',
            '\r\n\r\n',
            'ID  CATEGORY  DESCRIPTION          ALARM TYPE             DATE    TIME\r\n',
            'D 8  OTHER    VEEDER ROOT (FMS)    ALARM CLEAR WARNING  \r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I11400():
    return "".join(
        [
            '\x01\r\nI11400\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'CLEARED ALARMS REPORT',
            '\r\n\r\n',
            'ID  CATEGORY  DESCRIPTION          ALARM TYPE           STATE    DATE    TIME\r\n',
            'Q 4 OTHER     DIESEL               PERIODIC LINE FAIL   CLEAR   7-09-18  2:49PM\r\n',
            'Q 4 OTHER     DIESEL               PLLD SHUTDOWN ALARM  CLEAR   6-19-18  9:01AM\r\n',
            'Q 4 OTHER     DIESEL               GROSS LINE FAIL      CLEAR   6-19-18  9:01AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   5-10-18 11:29AM\r\n',
            'Q 3 OTHER     SUPREME              GROSS LINE FAIL      CLEAR   5-10-18 11:29AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        CLEAR   5-10-18 11:24AM\r\n',
            'Q 4 OTHER     DIESEL               PLLD SHUTDOWN ALARM  CLEAR   4-19-18 11:34AM\r\n',
            'Q 4 OTHER     DIESEL               GROSS LINE FAIL      CLEAR   4-19-18 11:34AM\r\n',
            'Q 2 OTHER     PLUS                 PLLD SHUTDOWN ALARM  CLEAR   4-19-18 11:33AM\r\n',
            'Q 2 OTHER     PLUS                 GROSS LINE FAIL      CLEAR   4-19-18 11:33AM\r\n',
            'Q 1 OTHER     REGULAR              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 11:33AM\r\n',
            'Q 1 OTHER     REGULAR              GROSS LINE FAIL      CLEAR   4-19-18 11:33AM\r\n',
            'L 2 ANNULAR   PLUS ANNULAR         FUEL ALARM           CLEAR   4-19-18 11:09AM\r\n',
            'L 1 ANNULAR   REGULAR ANNULAR      FUEL ALARM           CLEAR   4-19-18 11:01AM\r\n',
            'L 4 ANNULAR   DIESEL ANNULAR       FUEL ALARM           CLEAR   4-19-18 10:55AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        CLEAR   4-19-18 10:46AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              WATER ALARM          CLEAR   4-19-18 10:45AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              FUEL ALARM           CLEAR   4-19-18 10:45AM\r\n',
            's 8 OTHER     7,8 PAN              INSTALL ALARM        CLEAR   4-19-18 10:45AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:43AM\r\n',
            's 6 OTHER     3,4 PAN              WATER ALARM          CLEAR   4-19-18 10:43AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:42AM\r\n',
            's 6 OTHER     3,4 PAN              FUEL ALARM           CLEAR   4-19-18 10:42AM\r\n',
            's 7 OTHER     5,6 PAN-DIESEL       WATER ALARM          CLEAR   4-19-18 10:41AM\r\n',
            's 7 OTHER     5,6 PAN-DIESEL       FUEL ALARM           CLEAR   4-19-18 10:41AM\r\n',
            'Q 3 OTHER     SUPREME              PLLD SHUTDOWN ALARM  CLEAR   4-19-18 10:40AM\r\n',
            's 5 OTHER     1,2 PAN              WATER ALARM          CLEAR   4-19-18 10:40AM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      CLEAR   8-02-18  5:36AM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   7-24-18  4:17PM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      CLEAR   6-29-18  5:40PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   6-20-18 12:15AM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   6-14-18  3:11PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   6-06-18  5:50PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   5-18-18  6:11AM\r\n',
            '    SYSTEM                         PAPER OUT            CLEAR   5-18-18  6:11AM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   5-15-18 10:03PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   5-15-18  9:58PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   5-11-18  3:08PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   5-11-18  3:07PM\r\n',
            'T 4 TANK      DIESEL               DELIVERY NEEDED      CLEAR   5-08-18  1:08PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-26-18 10:47PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-23-18  8:34PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   4-20-18  6:15PM\r\n',
            's 1 OTHER     REGULAR STP SUMP     WATER WARNING        CLEAR   4-19-18 10:31AM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-14-18 11:34PM\r\n',
            'T 3 TANK      SUPREME              DELIVERY NEEDED      CLEAR   4-10-18  9:03PM\r\n',
            'T 1 TANK      REGULAR              DELIVERY NEEDED      CLEAR   4-04-18 12:33AM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PAPER OUT            CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PRINTER ERROR        CLEAR   3-30-18  9:58PM\r\n',
            '    SYSTEM                         PAPER OUT            CLEAR   3-30-18  9:58PM\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20100():
    return "".join(
        [
            "\x01\r\nI20100\r\n",
            now(),
            "\r\n\r\n",
            module_configuration()["company_name_address"],
            "\r\n\r\n",
            "IN-TANK INVENTORY       \r\n",
            "\r\n",
            "TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP\r\n",
            "  1  REGULAR               1693         0     9755    18.75     0.00    76.26\r\n",
            "  2  PLUS                  1788         0     6003    25.65     0.89    74.02\r\n",
            "  3  SUPREME               1748         0     7871    21.71     0.76    75.99\r\n",
            "  4  DIESEL                2147         0     7472    25.04     0.00    75.48\r\n",
            "\r\n",
            "\x03"
        ]
    )
