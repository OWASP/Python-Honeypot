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


def I20200():
    return "".join(
        [
            '\x01\r\nI20200\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'DELIVERY REPORT',
            '\r\n\r\n',
            'T 1:REGULAR\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  7, 2018  5:29 AM      9001       8908  0.00       74.67   65.05\r\n',
            '    START: AUG  7, 2018  4:55 AM      1693       1674  0.00       76.24   18.75\r\n',
            '   AMOUNT:                            7308       7234\r\n\r\n',
            '      END: AUG  4, 2018 10:03 AM      7816       7736  0.00       74.62   57.41\r\n',
            '    START: AUG  4, 2018  9:38 AM      2099       2076  0.00       75.67   21.76\r\n',
            '   AMOUNT:                            5717       5660\r\n\r\n',
            '      END: AUG  2, 2018  5:53 AM      7564       7488  0.00       74.18   55.85\r\n',
            '    START: AUG  2, 2018  5:35 AM      2517       2488  0.00       76.30   24.69\r\n',
            '   AMOUNT:                            5047       5000\r\n\r\n',
            '      END: AUG  1, 2018  1:23 AM      5147       5087  0.00       76.40   41.31\r\n',
            '    START: AUG  1, 2018  1:09 AM      2452       2419  0.00       78.47   24.24\r\n',
            '   AMOUNT:                            2695       2668\r\n\r\n',
            '      END: JUL 29, 2018  1:04 PM      8923       8809  0.00       78.22   64.53\r\n',
            '    START: JUL 29, 2018 12:32 PM      1214       1198  0.00       77.64   14.93\r\n',
            '   AMOUNT:                            7709       7611\r\n\r\n',
            '      END: JUL 25, 2018  2:22 PM      9923       9816  0.00       75.38   71.58\r\n',
            '    START: JUL 25, 2018  1:54 PM      2162       2138  0.00       75.73   22.21\r\n',
            '   AMOUNT:                            7761       7678\r\n\r\n',
            '      END: JUL 24, 2018  4:29 PM      4070       4024  0.00       75.96   34.75\r\n',
            '    START: JUL 24, 2018  4:16 PM       810        800  0.00       77.38   11.35\r\n',
            '   AMOUNT:                            3260       3224\r\n\r\n',
            '      END: JUL 21, 2018  9:05 PM      6562       6506  0.00       72.05   49.78\r\n',
            '    START: JUL 21, 2018  8:41 PM      1558       1537  0.00       78.74   17.71\r\n',
            '   AMOUNT:                            5004       4969\r\n\r\n',
            '      END: JUL 18, 2018  2:27 PM      9446       9324  0.00       78.47   68.11\r\n',
            '    START: JUL 18, 2018  2:00 PM      1662       1643  0.00       76.02   18.51\r\n',
            '   AMOUNT:                            7784       7681\r\n\r\n',
            '      END: JUL 17, 2018  2:35 AM      5632       5572  0.00       74.93   44.22\r\n',
            '    START: JUL 17, 2018  2:19 AM      1439       1423  0.00       75.78   16.77\r\n',
            '   AMOUNT:                            4193       4149\r\n\r\n',
            'T 2:PLUS\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  4, 2018  9:50 AM      2583       2554  0.89       75.49   33.18\r\n',
            '    START: AUG  4, 2018  9:38 AM      1387       1373  0.89       74.06   21.55\r\n',
            '   AMOUNT:                            1196       1181\r\n\r\n',
            '      END: AUG  1, 2018  1:21 AM      2510       2483  0.89       74.72   32.52\r\n',
            '    START: AUG  1, 2018  1:10 AM       821        812  0.90       74.48   15.10\r\n',
            '   AMOUNT:                            1689       1671\r\n\r\n',
            '      END: JUL 26, 2018  4:17 AM      2569       2544  0.90       73.61   33.06\r\n',
            '    START: JUL 26, 2018  4:05 AM       871        862  0.89       74.07   15.72\r\n',
            '   AMOUNT:                            1698       1682\r\n\r\n',
            '      END: JUL 21, 2018  9:01 PM      1903       1887  0.89       71.50   26.78\r\n',
            '    START: JUL 21, 2018  8:50 PM       902        893  0.84       73.68   16.09\r\n',
            '   AMOUNT:                            1001        994\r\n\r\n',
            '      END: JUL 14, 2018  7:02 AM      2966       2938  0.85       73.21   36.64\r\n',
            '    START: JUL 14, 2018  6:53 AM      1956       1939  0.88       71.84   27.30\r\n',
            '   AMOUNT:                            1010        999\r\n\r\n',
            '      END: JUL 11, 2018  1:46 AM      2893       2865  0.88       73.75   35.98\r\n',
            '    START: JUL 11, 2018  1:34 AM      1192       1182  0.90       71.36   19.42\r\n',
            '   AMOUNT:                            1701       1683\r\n\r\n',
            '      END: JUL  2, 2018  6:01 AM      3040       3013  0.89       72.37   37.29\r\n',
            '    START: JUL  2, 2018  5:51 AM      1344       1333  0.90       70.47   21.08\r\n',
            '   AMOUNT:                            1696       1680\r\n\r\n',
            '      END: JUN 27, 2018  4:50 AM      2709       2687  0.90       71.63   34.33\r\n',
            '    START: JUN 27, 2018  4:41 AM      1682       1668  0.92       71.49   24.60\r\n',
            '   AMOUNT:                            1027       1019\r\n\r\n',
            '      END: JUN 24, 2018  3:33 PM      2352       2328  0.88       74.07   31.06\r\n',
            '    START: JUN 24, 2018  3:24 PM      1352       1342  0.89       70.32   21.17\r\n',
            '   AMOUNT:                            1000        986\r\n\r\n',
            '      END: JUN 21, 2018 11:29 PM      2055       2037  0.88       71.97   28.26\r\n',
            '    START: JUN 21, 2018 11:18 PM      1061       1053  0.89       70.07   17.95\r\n',
            '   AMOUNT:                             994        984\r\n\r\n',
            'T 3:SUPREME\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  7, 2018  5:09 AM      2991       2955  0.76       76.83   31.61\r\n',
            '    START: AUG  7, 2018  5:01 AM      1748       1728  0.76       75.98   21.71\r\n',
            '   AMOUNT:                            1243       1227\r\n\r\n',
            '      END: AUG  4, 2018  9:55 AM      2911       2874  0.77       77.51   31.01\r\n',
            '    START: AUG  4, 2018  9:45 AM      1180       1167  0.76       76.00   16.59\r\n',
            '   AMOUNT:                            1731       1707\r\n\r\n',
            '      END: AUG  2, 2018  5:52 AM      1979       1956  0.77       76.39   23.66\r\n',
            '    START: AUG  2, 2018  5:45 AM       987        975  0.77       76.33   14.70\r\n',
            '   AMOUNT:                             992        981\r\n\r\n',
            '      END: JUL 29, 2018 12:45 PM      2330       2300  0.77       78.02   26.51\r\n',
            '    START: JUL 29, 2018 12:34 PM      1335       1319  0.76       76.17   18.04\r\n',
            '   AMOUNT:                             995        981\r\n\r\n',
            '      END: JUL 25, 2018  1:57 PM      2908       2871  0.77       77.83   30.99\r\n',
            '    START: JUL 25, 2018  1:51 PM      1913       1890  0.76       76.62   23.11\r\n',
            '   AMOUNT:                             995        981\r\n\r\n',
            '      END: JUL 24, 2018  4:33 PM      2103       2078  0.77       76.49   24.68\r\n',
            '    START: JUL 24, 2018  4:25 PM      1099       1086  0.77       75.86   15.81\r\n',
            '   AMOUNT:                            1004        992\r\n\r\n',
            '      END: JUL 18, 2018  2:03 PM      3212       3175  0.76       76.34   33.27\r\n',
            '    START: JUL 18, 2018  1:54 PM      2217       2196  0.76       73.43   25.61\r\n',
            '   AMOUNT:                             995        979\r\n\r\n',
            '      END: JUL 14, 2018  7:05 AM      3477       3440  0.76       75.05   35.22\r\n',
            '    START: JUL 14, 2018  6:52 AM      1789       1771  0.76       73.53   22.06\r\n',
            '   AMOUNT:                            1688       1669\r\n\r\n',
            '      END: JUL 11, 2018  1:49 AM      3150       3118  0.76       74.63   32.81\r\n',
            '    START: JUL 11, 2018  1:40 AM      1954       1936  0.76       72.58   23.45\r\n',
            '   AMOUNT:                            1196       1182\r\n\r\n',
            '      END: JUL  7, 2018  5:41 AM      3247       3216  0.76       73.58   33.53\r\n',
            '    START: JUL  7, 2018  5:30 AM      1312       1300  0.76       72.58   17.83\r\n',
            '   AMOUNT:                            1935       1916\r\n\r\n',
            'T 4:DIESEL\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  2, 2018  5:51 AM      3267       3240  0.00       77.40   33.67\r\n',
            '    START: AUG  2, 2018  5:36 AM       988        980  0.00       76.85   14.70\r\n',
            '   AMOUNT:                            2279       2260\r\n\r\n',
            '      END: JUL 21, 2018  8:54 PM      3399       3378  0.00       72.94   34.65\r\n',
            '    START: JUL 21, 2018  8:40 PM      1117       1108  0.00       76.97   15.98\r\n',
            '   AMOUNT:                            2282       2270\r\n\r\n',
            '      END: JUL  9, 2018  3:02 AM      3662       3639  0.00       73.90   36.57\r\n',
            '    START: JUL  9, 2018  2:39 AM      1376       1367  0.00       75.00   18.42\r\n',
            '   AMOUNT:                            2286       2272\r\n\r\n',
            '      END: JUN 29, 2018  5:52 PM      2979       2945  0.00       84.83   31.52\r\n',
            '    START: JUN 29, 2018  5:39 PM       697        692  0.00       74.63   11.62\r\n',
            '   AMOUNT:                            2282       2253\r\n\r\n',
            '      END: JUN 20, 2018 12:18 AM      3461       3437  0.00       75.22   35.10\r\n',
            '    START: JUN 20, 2018 12:04 AM      1176       1170  0.00       71.16   16.55\r\n',
            '   AMOUNT:                            2285       2267\r\n\r\n',
            '      END: JUN 12, 2018  4:22 AM      3785       3772  0.00       67.46   37.46\r\n',
            '    START: JUN 12, 2018  4:07 AM      1316       1309  0.00       70.96   17.86\r\n',
            '   AMOUNT:                            2469       2463\r\n\r\n',
            '      END: JUN  4, 2018  6:35 PM      3391       3364  0.00       77.20   34.59\r\n',
            '    START: JUN  4, 2018  6:22 PM      1108       1103  0.00       69.30   15.89\r\n',
            '   AMOUNT:                            2283       2261\r\n\r\n',
            '      END: MAY 23, 2018  9:06 AM      3667       3652  0.00       68.84   36.61\r\n',
            '    START: MAY 23, 2018  8:51 AM      1381       1376  0.00       67.20   18.46\r\n',
            '   AMOUNT:                            2286       2276\r\n\r\n',
            '      END: MAY 13, 2018  6:20 AM      3770       3756  0.00       67.62   37.35\r\n',
            '    START: MAY 13, 2018  6:07 AM      1485       1480  0.00       66.82   19.41\r\n',
            '   AMOUNT:                            2285       2276\r\n\r\n',
            '      END: MAY  8, 2018  1:19 PM      3133       3118  0.00       69.97   32.68\r\n',
            '    START: MAY  8, 2018  1:07 PM       857        855  0.00       64.64   13.36\r\n',
            '   AMOUNT:                            2276       2263\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20300():
    return "".join(
        [
            '\x01\r\nI20300\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'TANK 1    REGULAR                \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n',
            '\r\n\r\n',
            'TANK 2    PLUS                   \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n',
            '\r\n\r\n',
            'TANK 3    SUPREME                \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n',
            '\r\n\r\n',
            'TANK 4    DIESEL                 \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n',
            '\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20400():
    return "".join(
        [
            '\x01\r\nI20400\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            ' SHIFT REPORT \r\n\r\n',
            'SHIFT 1 TIME: 12:00 AM        \r\n\r\n',
            'TANK PRODUCT\r\n\r\n',
            '  1  REGULAR                VOLUME TC VOLUME  ULLAGE  HEIGHT  WATER   TEMP\r\n',
            'SHIFT  1 STARTING VALUES      4672      4621    6776   38.44   0.00  75.53\r\n',
            '         ENDING VALUES        1724      1704    9724   18.99   0.00  76.41\r\n',
            '         DELIVERY VALUE          0\r\n',
            '         TOTALS               2948\r\n\r\n',
            '  2  PLUS                   VOLUME TC VOLUME  ULLAGE  HEIGHT  WATER   TEMP\r\n',
            'SHIFT  1 STARTING VALUES      2133      2111    5658   29.00   0.89  74.16\r\n',
            '         ENDING VALUES        1788      1770    6003   25.66   0.89  74.18\r\n',
            '         DELIVERY VALUE          0\r\n',
            '         TOTALS                345\r\n\r\n',
            '  3  SUPREME                VOLUME TC VOLUME  ULLAGE  HEIGHT  WATER   TEMP\r\n',
            'SHIFT  1 STARTING VALUES      2204      2178    7415   25.50   0.76  76.20\r\n',
            '         ENDING VALUES        1765      1745    7854   21.86   0.76  76.13\r\n',
            '         DELIVERY VALUE          0\r\n',
            '         TOTALS                439\r\n\r\n',
            '  4  DIESEL                 VOLUME TC VOLUME  ULLAGE  HEIGHT  WATER   TEMP\r\n',
            'SHIFT  1 STARTING VALUES      2459      2442    7160   27.53   0.00  75.20\r\n',
            '         ENDING VALUES        2147      2132    7472   25.04   0.00  75.58\r\n',
            '         DELIVERY VALUE          0\r\n',
            '         TOTALS                312\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20500():
    return "".join(
        [
            '\x01\r\nI20500\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'TANK   PRODUCT                 STATUS\r\n\r\n',
            '  1    REGULAR                 NORMAL\r\n\r\n',
            '  2    PLUS                    NORMAL\r\n\r\n  3',
            '    SUPREME                 NORMAL\r\n\r\n',
            '  4    DIESEL                  NORMAL\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20600():
    return "".join(
        [
            '\x01\r\nI20600\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n\r\n',
            'TANK ALARM HISTORY\r\n\r\n',
            'TANK 1  REGULAR             \r\n\r\n',
            '     OVERFILL ALARM           FEB  8, 2018  5:29 AM\r\n\r\n',
            '     LOW PRODUCT ALARM        OCT 12, 2017  2:32 PM\r\n',
            '                              SEP 18, 2017  4:09 PM\r\n\r\n',
            '     SUDDEN LOSS ALARM        FEB 21, 2017  8:02 AM\r\n\r\n',
            '     PROBE OUT                FEB 21, 2017  8:02 AM\r\n\r\n',
            '     DELIVERY NEEDED          JUL 24, 2018  1:36 PM\r\n',
            '                              JUN 14, 2018  1:56 PM\r\n',
            '                              MAY 15, 2018  6:56 PM\r\n\r\n',
            'TANK 2  PLUS                \r\n\r\n',
            '     HIGH WATER ALARM         APR 20, 2017  2:10 PM\r\n\r\n',
            '     OVERFILL ALARM           APR 20, 2017  2:03 PM\r\n\r\n',
            '     LOW PRODUCT ALARM        APR 20, 2017  2:01 PM\r\n',
            '                              FEB 21, 2017  8:21 AM\r\n\r\n',
            '     HIGH PRODUCT ALARM       APR 20, 2017  2:04 PM\r\n\r\n',
            '     INVALID FUEL LEVEL       APR 20, 2017  2:01 PM\r\n\r\n',
            '     PROBE OUT                APR 20, 2017  2:33 PM\r\n',
            '                              APR 20, 2017  2:00 PM\r\n\r\n',
            '     HIGH WATER WARNING       APR 20, 2017  2:10 PM\r\n\r\n',
            '     DELIVERY NEEDED          OCT  7, 2017  7:12 PM\r\n',
            '                              SEP 18, 2017  5:44 PM\r\n',
            '                              JUN 26, 2017  5:31 PM\r\n\r\n',
            '     MAX PRODUCT ALARM        APR 20, 2017  2:04 PM\r\n\r\n',
            'TANK 3  SUPREME             \r\n\r\n',
            '     HIGH WATER ALARM         APR 20, 2017  2:11 PM\r\n\r\n',
            '     OVERFILL ALARM           APR 20, 2017  2:04 PM\r\n\r\n',
            '     LOW PRODUCT ALARM        MAY 20, 2017  4:38 PM\r\n',
            '                              APR 20, 2017  2:03 PM\r\n\r\n',
            '     SUDDEN LOSS ALARM        APR 20, 2017  2:02 PM\r\n\r\n',
            '     HIGH PRODUCT ALARM       APR 20, 2017  2:04 PM\r\n\r\n',
            '     INVALID FUEL LEVEL       APR 20, 2017  2:03 PM\r\n\r\n',
            '     PROBE OUT                APR 20, 2017  2:30 PM\r\n',
            '                              APR 20, 2017  2:02 PM\r\n\r\n',
            '     HIGH WATER WARNING       APR 20, 2017  2:11 PM\r\n\r\n',
            '     DELIVERY NEEDED          JUN 19, 2018  6:29 PM\r\n',
            '                              JUN  6, 2018  1:52 PM\r\n',
            '                              MAY 15, 2018  6:49 PM\r\n\r\n',
            '     MAX PRODUCT ALARM        APR 20, 2017  2:04 PM\r\n\r\n',
            'TANK 4  DIESEL              \r\n\r\n',
            '     LOW PRODUCT ALARM        AUG 11, 2017  9:40 AM\r\n',
            '                              AUG 11, 2017  9:02 AM\r\n',
            '                              AUG 11, 2017  8:55 AM\r\n\r\n',
            '     SUDDEN LOSS ALARM        AUG 11, 2017  8:55 AM\r\n\r\n',
            '     INVALID FUEL LEVEL       AUG 11, 2017  9:40 AM\r\n',
            '                              AUG 11, 2017  9:02 AM\r\n',
            '                              AUG 11, 2017  8:55 AM\r\n\r\n',
            '     PROBE OUT                AUG 11, 2017  8:56 AM\r\n\r\n',
            '     DELIVERY NEEDED          AUG  2, 2018  5:09 AM\r\n',
            '                              JUN 29, 2018  2:58 AM\r\n',
            '                              MAY  7, 2018  3:16 PM\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20700():
    return "".join(
        [
            '\x01\r\nI20700\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n\r\n',
            'TANK LEAK TEST HISTORY\r\n\r\n',
            'T 1:REGULAR\r\n\r\n',
            'LAST GROSS TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST ANNUAL TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'FULLEST ANNUAL TEST PASS\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST PERIODIC TEST PASS:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n\r\n',
            'FULLEST PERIODIC TEST\r\n',
            'PASSED EACH MONTH:\r\n\r\n',
            'TEST START TIME            HOURS    VOLUME   % VOLUME   TEST TYPE\r\n\r\n\r\n\r\n',
            'TANK LEAK TEST HISTORY\r\n\r\n',
            'T 2:PLUS\r\n\r\n',
            'LAST GROSS TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST ANNUAL TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'FULLEST ANNUAL TEST PASS\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST PERIODIC TEST PASS:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n\r\n',
            'FULLEST PERIODIC TEST\r\n',
            'PASSED EACH MONTH:\r\n\r\n',
            'TEST START TIME            HOURS    VOLUME   % VOLUME   TEST TYPE\r\n\r\n\r\n\r\n',
            'TANK LEAK TEST HISTORY\r\n\r\n',
            'T 3:SUPREME\r\n\r\n',
            'LAST GROSS TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST ANNUAL TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'FULLEST ANNUAL TEST PASS\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST PERIODIC TEST PASS:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n\r\n',
            'FULLEST PERIODIC TEST\r\n',
            'PASSED EACH MONTH:\r\n\r\n',
            'TEST START TIME            HOURS    VOLUME   % VOLUME   TEST TYPE\r\n\r\n\r\n\r\n',
            'TANK LEAK TEST HISTORY\r\n\r\n',
            'T 4:DIESEL\r\n\r\n',
            'LAST GROSS TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST ANNUAL TEST PASSED:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'FULLEST ANNUAL TEST PASS\r\n\r\n',
            'NO TEST PASSED\r\n\r\n',
            'LAST PERIODIC TEST PASS:\r\n\r\n',
            'NO TEST PASSED\r\n\r\n\r\n',
            'FULLEST PERIODIC TEST\r\n',
            'PASSED EACH MONTH:\r\n\r\n',
            'TEST START TIME            HOURS    VOLUME   % VOLUME   TEST TYPE\r\n\r\n\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20800():
    return "".join(
        [
            '\x01\r\nI20800\r\n',
            now(),
            '\r\n\r\n',
            'PREVIOUS IN TANK LEAK TEST RESULTS\r\n\r\n',
            'TANK 1    REGULAR                \r\n',
            'TEST TYPE  START TIME              RESULT     RATE  HOURS  VOLUME\r\n',
            ' ANNUAL    NO TEST DATA AVAILABLE\r\n',
            ' PERIODIC  NO TEST DATA AVAILABLE\r\n',
            ' GROSS     NO TEST DATA AVAILABLE\r\n\r\n',
            'TANK 2    PLUS                   \r\n',
            'TEST TYPE  START TIME              RESULT     RATE  HOURS  VOLUME\r\n',
            ' ANNUAL    NO TEST DATA AVAILABLE\r\n',
            ' PERIODIC  NO TEST DATA AVAILABLE\r\n',
            ' GROSS     NO TEST DATA AVAILABLE\r\n\r\n',
            'TANK 3    SUPREME                \r\n',
            'TEST TYPE  START TIME              RESULT     RATE  HOURS  VOLUME\r\n',
            ' ANNUAL    NO TEST DATA AVAILABLE\r\n',
            ' PERIODIC  NO TEST DATA AVAILABLE\r\n',
            ' GROSS     NO TEST DATA AVAILABLE\r\n\r\n',
            'TANK 4    DIESEL                 \r\n',
            'TEST TYPE  START TIME              RESULT     RATE  HOURS  VOLUME\r\n',
            ' ANNUAL    NO TEST DATA AVAILABLE\r\n',
            ' PERIODIC  NO TEST DATA AVAILABLE\r\n',
            ' GROSS     NO TEST DATA AVAILABLE\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20900():
    return "".join(
        [
            '\x01\r\nI20900\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'TANK 1    REGULAR                \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n\r\n\r\n',
            'TANK 2    PLUS                   \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n\r\n\r\n',
            'TANK 3    SUPREME                \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n\r\n\r\n',
            'TANK 4    DIESEL                 \r\n',
            '    TEST STATUS: OFF   \r\n',
            'LEAK DATA NOT AVAILABLE ON THIS TANK\r\n\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20C00():
    return "".join(
        [
            '\x01\r\nI20C00\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'LAST DELIVERY REPORT\r\n\r\n',
            'T 1:REGULAR\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  7, 2018  5:29 AM      9001       8908  0.00       74.67   65.05\r\n',
            '    START: AUG  7, 2018  4:55 AM      1693       1674  0.00       76.24   18.75\r\n',
            '   AMOUNT:                            7308       7234\r\n\r\n',
            'T 2:PLUS\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  4, 2018  9:50 AM      2583       2554  0.89       75.49   33.18\r\n',
            '    START: AUG  4, 2018  9:38 AM      1387       1373  0.89       74.06   21.55\r\n',
            '   AMOUNT:                            1196       1181\r\n\r\n',
            'T 3:SUPREME\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  7, 2018  5:09 AM      2991       2955  0.76       76.83   31.61\r\n',
            '    START: AUG  7, 2018  5:01 AM      1748       1728  0.76       75.98   21.71\r\n',
            '   AMOUNT:                            1243       1227\r\n\r\n',
            'T 4:DIESEL\r\n',
            'INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT\r\n\r\n',
            '      END: AUG  2, 2018  5:51 AM      3267       3240  0.00       77.40   33.67\r\n',
            '    START: AUG  2, 2018  5:36 AM       988        980  0.00       76.85   14.70\r\n',
            '   AMOUNT:                            2279       2260\r\n\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I20D00():
    return "".join(
        [
            '\x01\r\nI20D00\r\n',
            now(),
            '\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I25100():
    return "".join(
        [
            '\x01\r\nI25100\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'CSLD TEST RESULTS\r\n',
            'TANK PRODUCT                RESULT\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I30100():
    return "".join(
        [
            '\x01\r\nI30100\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'LIQUID STATUS REPORT\r\n\r\n',
            'SENSOR  LOCATION               STATUS\r\n',
            '     1  REGULAR ANNULAR        SENSOR NORMAL\r\n',
            '     2  PLUS ANNULAR           SENSOR NORMAL\r\n',
            '     3  SUPER ANNULAR          SENSOR NORMAL\r\n',
            '     4  DIESEL ANNULAR         SENSOR NORMAL\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I30200():
    return "".join(
        [
            '\x01\r\nI30200\r\n',
            now(),
            '\r\n\r\n',
            module_configuration()["company_name_address"],
            '\r\n\r\n',
            'LIQUID ALARM HISTORY REPORT\r\n\r\n',
            'SENSOR  LOCATION\r\n',
            '     1  REGULAR ANNULAR      \r\n',
            '        APR 19, 2018 11:00 AM         FUEL ALARM\r\n',
            '        APR 20, 2017 12:49 PM         FUEL ALARM\r\n',
            '        JAN  5, 2017 10:15 AM         SETUP DATA WARNING \r\n',
            '     2  PLUS ANNULAR         \r\n',
            '        APR 19, 2018 11:06 AM         FUEL ALARM\r\n',
            '        APR 20, 2017 12:54 PM         FUEL ALARM\r\n',
            '        JAN  5, 2017 10:15 AM         SETUP DATA WARNING \r\n',
            '     3  SUPER ANNULAR        \r\n',
            '        APR 20, 2017  1:04 PM         FUEL ALARM\r\n',
            '        APR 20, 2017  1:03 PM         FUEL ALARM\r\n',
            '        APR 20, 2017  1:01 PM         FUEL ALARM\r\n',
            '     4  DIESEL ANNULAR       \r\n',
            '        APR 19, 2018 10:51 AM         FUEL ALARM\r\n',
            '        APR 20, 2017  1:13 PM         FUEL ALARM\r\n',
            '        JAN  5, 2017 10:15 AM         SETUP DATA WARNING \r\n',
            '\r\n',
            '\x03'
        ]
    )


def I50100():
    return "".join(
        [
            '\x01\r\nI50100\r\n',
            now(),
            '\r\n\r\n',
            'SYSTEM DATE AND TIME\r\n\r\n',
            '\r\n',
            '\x03',
        ]
    )


def I50A00():
    return "".join(
        [
            '\x01\r\nI50A00\r\n',
            now(),
            '\r\n\r\n',
            'ANNUAL TEST WARNING: DAYS = 355\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I50B00():
    return "".join(
        [
            '\x01\r\nI50B00\r\n',
            now(),
            '\r\n\r\n',
            'ANNUAL TEST ALARM: DAYS = 365\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I50C00():
    return "".join(
        [
            '\x01\r\nI50C00\r\n',
            now(),
            '\r\n\r\n',
            'REMOTE PRINTER\r\n',
            'DISABLED\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I50E00():
    return "".join(
        [
            '\x01\r\nI50E00\r\n',
            now(),
            '\r\n\r\n',
            'TEMP COMPENSATION\r\n',
            'VALUE (DEG F ):   60.0\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I50F00():
    return "".join(
        [
            '\x01\r\nI50F00\r\n',
            now(),
            '\r\n\r\n',
            'MON DD YYYY HH:MM:SS xM\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I51400():
    return "".join(
        [
            '\x01\r\nI51400\r\n',
            now(),
            '\r\n\r\n',
            'H-PROTOCOL DATA FORMAT\r\n',
            'HEIGHT\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I51700():
    return "".join(
        [
            '\x01\r\nI51700\r\n',
            now(),
            '\r\n\r\n',
            'SYSTEM TYPE AND LANGUAGE FLAG\r\n\r\n',
            'SYSTEM UNITS\r\n',
            ' U.S.\r\n',
            'SYSTEM LANGUAGE\r\n',
            ' ENGLISH\r\n',
            'SYSTEM DATE/TIME FORMAT\r\n',
            'MON DD YYYY HH:MM:SS xM\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I51A00():
    return "".join(
        [
            '\x01\r\nI51A00\r\n',
            now(),
            '\r\n\r\n',
            'DAYLIGHT SAVING TIME\r\n',
            'ENABLED ON\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I51B00():
    return "".join(
        [
            '\x01\r\nI51B00\r\n',
            now(),
            '\r\n\r\n',
            'DAYLIGHT SAVING TIME\r\n\r\n',
            'START DATE    MAR   WEEK 2   SUN   2:00 AM\r\n\r\n',
            'END DATE      NOV   WEEK 1   SUN   2:00 AM\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I51C00():
    return "".join(
        [
            '\x01\r\nI51C00\r\n',
            now(),
            '\r\n\r\n',
            'TICKETED DELIVERY\r\n',
            'DISABLED\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I51F00():
    return "".join(
        [
            '\x01\r\nI51F00\r\n',
            now(),
            '\r\n\r\n',
            'EURO PROTOCOL PREFIX\r\n',
            'S\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I53100():
    return "".join(
        [
            '\x01\r\nI53100\r\n',
            now(),
            '\r\n\r\n',
            'RS-232 END OF MESSAGE\r\n',
            'DISABLED\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I60100():
    return "".join(
        [
            '\x01\r\nI60100\r\n',
            now(),
            '\r\n\r\n',
            'TANK CONFIGURATION',
            '\r\n\r\n',
            'DEVICE  LABEL                  CONFIGURED\r\n',
            '     1  REGULAR                ON\r\n',
            '     2  PLUS                   ON\r\n',
            '     3  SUPREME                ON\r\n',
            '     4  DIESEL                 ON\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I60200():
    return "".join(
        [
            '\x01\r\nI60200\r\n',
            now(),
            '\r\n\r\n',
            'TANK PRODUCT LABEL',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL          \r\n',
            ' 1     REGULAR                   \r\n',
            ' 2     PLUS                      \r\n',
            ' 3     SUPREME                   \r\n',
            ' 4     DIESEL                    ',
            '\r\n',
            '\x03'
        ]
    )


def I60300():
    return "".join(
        [
            '\x01\r\nI60300\r\n',
            now(),
            '\r\n\r\n',
            'TANK PRODUCT CODE',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL          \r\n',
            ' 1     REGULAR                   1\r\n',
            ' 2     PLUS                      2\r\n',
            ' 3     SUPREME                   3\r\n',
            ' 4     DIESEL                    4',
            '\r\n',
            '\x03'
        ]
    )


def I60400():
    return "".join(
        [
            '\x01\r\nI60400\r\n',
            now(),
            '\r\n\r\n',
            'TANK FULL VOLUME',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL             GALLONS\r\n',
            ' 1     REGULAR                    11682\r\n',
            ' 2     PLUS                        7950\r\n',
            ' 3     SUPREME                     9816\r\n',
            ' 4     DIESEL                      9816',
            '\r\n',
            '\x03'
        ]
    )


def I60500():
    return "".join(
        [
            '\x01\r\nI60500\r\n',
            now(),
            '\r\n\r\n',
            'TANK 4 POINT VOLUMES',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL                         GALLONS\r\n',
            ' 1     REGULAR                      11682    9479    5856    2243\r\n',
            ' 2     PLUS                          7950    6473    3986    1505\r\n',
            ' 3     SUPREME                       9816    7976    4921    1874\r\n',
            ' 4     DIESEL                        9816    7976    4921    1874\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I60600():
    return "".join(
        [
            '\x01\r\nI60600\r\n',
            now(),
            '\r\n\r\n',
            'TANK 20 POINT VOLUMES',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL                         GALLONS\r\n',
            ' 1     REGULAR                      11682       0       0       0\r\n',
            '                                        0    9479       0       0\r\n',
            '                                        0       0    5856       0\r\n',
            '                                        0       0       0    2243\r\n',
            '                                        0       0       0       0\r\n',
            ' 2     PLUS                          7950       0       0       0\r\n',
            '                                        0    6473       0       0\r\n',
            '                                        0       0    3986       0\r\n',
            '                                        0       0       0    1505\r\n',
            '                                        0       0       0       0\r\n',
            ' 3     SUPREME                       9816       0       0       0\r\n',
            '                                        0    7976       0       0\r\n',
            '                                        0       0    4921       0\r\n',
            '                                        0       0       0    1874\r\n',
            '                                        0       0       0       0\r\n',
            ' 4     DIESEL                        9816       0       0       0\r\n',
            '                                        0    7976       0       0\r\n',
            '                                        0       0    4921       0\r\n',
            '                                        0       0       0    1874\r\n',
            '                                        0       0       0       0\r\n',
            '\r\n',
            '\x03'
        ]
    )


def I60700():
    return "".join(
        [
            '\x01\r\nI60700\r\n',
            now(),
            '\r\n\r\n',
            'TANK DIAMETER',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL             INCHES\r\n',
            ' 1     REGULAR                    91.13\r\n',
            ' 2     PLUS                       91.13\r\n',
            ' 3     SUPREME                    91.13\r\n',
            ' 4     DIESEL                     91.13',
            '\r\n',
            '\x03'
        ]
    )


def I60800():
    return "".join(
        [
            '\x01\r\nI60800\r\n',
            now(),
            '\r\n\r\n',
            'TANK TILT',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL             INCHES\r\n',
            ' 1     REGULAR                     0.00\r\n',
            ' 2     PLUS                        0.00\r\n',
            ' 3     SUPREME                     0.00\r\n',
            ' 4     DIESEL                      0.00',
            '\r\n',
            '\x03'
        ]
    )


def I60900():
    return "".join(
        [
            '\x01\r\nI60900\r\n',
            now(),
            '\r\n\r\n',
            'TANK THERMAL COEFFICIENT',
            '\r\n\r\n',
            'TANK   PRODUCT LABEL          \r\n',
            ' 1     REGULAR                   0.000700\r\n',
            ' 2     PLUS                      0.000700\r\n',
            ' 3     SUPREME                   0.000700\r\n',
            ' 4     DIESEL                    0.000450',
            '\r\n',
            '\x03'
        ]
    )
