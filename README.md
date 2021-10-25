# HTTP sniffer challenge
Here is the work sample that was discussed (Remember the focus is on polish, detail, tests, and production quality).

* Create a simple console program that monitors HTTP traffic on your machine: Sniff network traffic to detect HTTP activity.
* Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what’s before the second ‘/’ in a URL. i.e. the section for “http://my.site.com/pages/create’ is “http://my.site.com/pages”), as well as interesting summary statistics on the traffic as a whole.
* Make sure a user can keep the console app running and monitor traffic on their machine.
* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = (value), triggered at (time)“.
* Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered.
* Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons.
* Write a test for the alerting logic.
* Explain how you’d improve on this application design.

# Design Choices

* project is written in python3
* choice is to use a 3rd party library for monitoring the HTTP traffic (scapy https://scapy.net)\
  in order to concentrate the challenge on the monitoring and alerting features.
* only HTTP, no HTTPs considered (and end-to-end encryption would prevent it unless going through \
  a man-in-the-middle proxy).

# Project code structure

Code is organized in packages and modules as follows:

* *src/interfaces*\
      Contains the definitions of all interfaces as abstract classes:\
         * *abstract_sniffer.py* = abstract HTTP traffic sniffer in charge of monitoring HTTP requests .
         * *abstract_collector.py* = abstract HTTP traffic collector in charge of collecting HTTP traffic.
         * *abstract_alert_manager.py* = abstract alert manager.
         * *abstract_view.py* = abstract view for displaying traffic and alerting information.
    Another valid possibility would be to put the interface of each class at the same level than its\
    implementation(s).

* *src/sniffers*\
  Contains the HTTP sniffer implementation which translates packet information to HTTP information.\     
  Uses the scapy 3rd party library.\
  Corresponds to *abstract_sniffer.py*.

* *src/collectors*\
 Contains the implementation of the HTTP traffic collector *basic_collector.py*.\
 Manages both highest hits and traffic history used for alerting of the HTTP traffic information relayed to it.\
 Corresponds to *abstract_collector.py*.

* *src/alert_managers*\
 Contains the implementation of the alert management logic.\
 The alerts are generated on the basis of the total traffic which is relayed periodically to\
 the alert manager by the controller. Thus only the logic (as a finite-state automaton) needs to be managed\
 by this class.
 Corresponds to *abstract_alert_manager.py*.

* *src/views*\
 Contains two console-based information display views for traffic highest hits and alerting.\
 *print_view.py* does basic printing in a scrolling terminal.\
 *curses_view.py* displays the traffic and alerting information is fixed "windows".\
 Note that the view is in charge of managing the fact that alerts must be memorized (up to some limit).
 It's probably not the best design choice.\
 Corresponds to *abstract_view.py*.

* *src/controllers*\
  Contains the implementation of the controller *controller.py* which manages the application workflow:
  * starts the sniffer and links its output to the HTTP traffic collector using a callback.
  * periodically (10 seconds by default) collects the traffic information from the HTTP traffic collector.
  * relays the traffic information to the alert manager and fetches the corresponding alert information (if any).
  * updates the view with the traffic information (highest hits and statistics) and alerting information.\
  Note there is no abstract class / interface for the controller - but there could be. 

# Main Data Structures and Objects

Most data objects (implemented as python dataclasses) are defined either in the abstraction / interface\
where they appear in the method signatures, or in implementation classes when only used internally to the module.

Note it would be better to put all such definitions into a specific *domain/* package as separate modules,\
instead of spreading them around. 

* *HTTPInfo* dataclass defined in *abstract_collector.py* represents a HTTP query information\
  as relayed from the sniffer to the HTTP collector. It defines the *extract_section* function responsible\
  for extracting sections from host and path information.
* *HitInfo* dataclass defined in *abstract_collector.py* represents information about a section number of hits
  over time, plus information about the last seen hit on the section. These objects are built from incoming\
  *HTTPInfos*.
* *TrafficInfo* dataclass defined in *basic_collector.py* and only used internally to this module in order to\ 
  represent an amount of traffic (in bytes) plus a timestamp. The *TrafficInfo*s are used to store the history\
  of the traffic information so that the HTTP traffic collector can be queried for reporting the total traffic over a\
  given time period (10 minutes by default).
* *AlertInfo* dataclass defined in *abstract_alert_manager.py* is used to represent the occurrence of an alert\
  or an alert recovery. It uses an *AlertStatus* enumeration for the three cases of no alert, over-threshold alert\
  and recovery alert. 

# Testing

Due to time constraints, the code base is not tested as exhaustively as it should be (far from it).

Still the *tests/* directory contains *test_alert_manager.py* which contains unit tests for the alerting logic\
implemented by the alert manager implementation (see *alert_managers/basic_alert_manager.py*). 

Plus a unit test *test_extract_section.py* for the section extraction method, because it's a bit tricky from a string manipulation POV.

Note that testing the alert manager is pretty simple due to it managing only the logic of the alerting transitions\
as a finite state automaton. In particular, the implementation of the alert manager consists of a single method\
besides its constructor:

```
def get_alert_info(self, traffic: int) -> Optional[AlertInfo]*
```

This function implements an automaton which, depending on the current state of the alerting status and the incoming\
traffic over the last time period, decides whether an alert should be emitted for 

* going over the threshold from a no-alert state
* recovering from an over-threshold state by the traffic going under the threshold

So for a good coverage the tests have to check:

* whether the over-threshold alert is emitted when the state changes from under to over threshold.
* whether the recovery alert is emitted when the state changes from over to under threshold.
* that no alert is emitted is the state does not change (under to under threshold, over to over threshold).  

The tests are implemented as is:

* Unit test *test_alert_manager_stays_under_threshold* tests the case where the traffic rises regularly but stays\ 
  under the alerting threshold. So this handles the fact that no alert should be emitted when traffic stays\
  under threshold.
* Unit test *test_alert_manager_goes_over_then_under_threshold* tests several cases (which is not ideal):
  * a over-threshold alert is emitted when going from under to over threshold
  * no alert is emitted as the traffic stays over the threshold
  * a recovery alert is emitted when the traffic then goes under the threshold
  * no alert is emitted as the traffic stays under the threshold

So in fact the first test could be removed because the second also tests "no alert from under to under threshold".
And the second test probably handles too much.

# How to improve the application design ?

* create specific modules for the domain objects like *HTTPInfo*, *HitInfo*, *AlertInfo*. 
* provide abstraction / interface for the controller also.
* move responsibility of managing historical alerts from the view class(es) to another class.
* write more unit tests and also split the alerting logic tests in more tests.
* provide better documentation of the class interactions and the MVC design pattern.

# Other notes

* This project took me more than double the expected time of 4 hours. And I would have spent more time for a 
  production ready application.
* Both the "print" view and the ncurses views have been tested on Windows, and in the Windows Linux subsystem.
* The script should run on a standard python3 installation starting from version 3.7 (cf. dataclasses), \
  provided scapy and ncurses are installed properly (scapy is a must, ncurses can be avoided if the print view \
  is used only).
* python 3.9 was used for development, as well as github and pycharm community edition. I can provide \
  the github repository if necessary.
* used pycharm linting capabilities, but did not use any other external tool, no test coverage measurement\
* (which would obviously be extremely low), no performance measurement, no stress tests.

# Some execution traces

The following traces were obtained by generating HTTP traffic using e.g. a python3 script POSTing small amount of data \
to HTTP public sites. The traffic limit is set to 10k bytes as alerting threshold.

**Important note: for the trace test, the information is displayed every 2 seconds (down from 10) and the alert is on 
a 20 seconds period (down from 120) !**

###Script used for generating traffic

```
import requests
import time

def do_req():
    for t in ["bing.fr", "bing.it", "bing.de"]:
        r = requests.post(f"http://{t}/some/path", data="0" * 1000)

def run():
     for x in range(10):
        do_req()
        time.sleep(1)

run()
```

### Trace

* no traffic at all to start with
* hits on bing.fr, bing.it and bing.de for 1k bytes each (information emitted every 2 seconds)
* after a few seconds traffic reaches 12k bytes which is over the 10k threshold, thus an alert is emitted
* the alert continues being emitted, while the total traffic continues to grow
* the traffic stops, so total traffic over the last 20 seconds goes under threshold, traffic recovery alert is emitted
* both alerts are still shown, despite highest hits stuck at 10 and no more traffic


```
start controller

Highest hits @ 2021-10-25 23:55:14.599781  
Highest hits @ 2021-10-25 23:55:16.609355  
Highest hits @ 2021-10-25 23:55:18.621628  
Highest hits @ 2021-10-25 23:55:20.632728  
Highest hits @ 2021-10-25 23:55:22.637590    
Highest hits @ 2021-10-25 23:55:24.637738 
bing.fr/some: hits 1 | total traffic 1000 | last request traffic 1000 @ 2021-10-25 23:55:24.488738  
Highest hits @ 2021-10-25 23:55:26.645618  
bing.fr/some: hits 2 | total traffic 2000 | last request traffic 1000 @ 2021-10-25 23:55:26.325632  
bing.it/some: hits 2 | total traffic 2000 | last request traffic 1000 @ 2021-10-25 23:55:26.513622  
bing.de/some: hits 1 | total traffic 1000 | last request traffic 1000 @ 2021-10-25 23:55:25.119895  
Highest hits @ 2021-10-25 23:55:28.650970  
bing.fr/some: hits 3 | total traffic 3000 | last request traffic 1000 @ 2021-10-25 23:55:27.817936  
bing.it/some: hits 3 | total traffic 3000 | last request traffic 1000 @ 2021-10-25 23:55:28.005946  
bing.de/some: hits 3 | total traffic 3000 | last request traffic 1000 @ 2021-10-25 23:55:28.195969  
Highest hits @ 2021-10-25 23:55:30.660807  
bing.fr/some: hits 4 | total traffic 4000 | last request traffic 1000 @ 2021-10-25 23:55:29.383633  
bing.it/some: hits 4 | total traffic 4000 | last request traffic 1000 @ 2021-10-25 23:55:29.571634  
bing.de/some: hits 4 | total traffic 4000 | last request traffic 1000 @ 2021-10-25 23:55:29.757636  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807
Highest hits @ 2021-10-25 23:55:32.676344
bing.fr/some: hits 6 | total traffic 6000 | last request traffic 1000 @ 2021-10-25 23:55:32.533313
bing.it/some: hits 5 | total traffic 5000 | last request traffic 1000 @ 2021-10-25 23:55:31.156306
bing.de/some: hits 5 | total traffic 5000 | last request traffic 1000 @ 2021-10-25 23:55:31.342335
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807
Highest hits @ 2021-10-25 23:55:34.684441  
bing.fr/some: hits 7 | total traffic 7000 | last request traffic 1000 @ 2021-10-25 23:55:34.039443  
bing.it/some: hits 7 | total traffic 7000 | last request traffic 1000 @ 2021-10-25 23:55:34.251440  
bing.de/some: hits 7 | total traffic 7000 | last request traffic 1000 @ 2021-10-25 23:55:34.373433  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:36.685386  
bing.fr/some: hits 8 | total traffic 8000 | last request traffic 1000 @ 2021-10-25 23:55:35.571311  
bing.it/some: hits 8 | total traffic 8000 | last request traffic 1000 @ 2021-10-25 23:55:35.761270  
bing.de/some: hits 8 | total traffic 8000 | last request traffic 1000 @ 2021-10-25 23:55:36.260344  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:38.687538  
bing.fr/some: hits 9 | total traffic 9000 | last request traffic 1000 @ 2021-10-25 23:55:37.461539  
bing.it/some: hits 9 | total traffic 9000 | last request traffic 1000 @ 2021-10-25 23:55:37.658571  
bing.de/some: hits 9 | total traffic 9000 | last request traffic 1000 @ 2021-10-25 23:55:37.840573    
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807    
Highest hits @ 2021-10-25 23:55:40.702410  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:42.711226  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:44.724778  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:46.734652  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:48.748389  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:50.758208  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:52.770291  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Highest hits @ 2021-10-25 23:55:54.780068  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Traffic recovered - hits = 9000, triggered at 2021-10-25 23:55:54.780069  
Highest hits @ 2021-10-25 23:55:56.793230  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Traffic recovered - hits = 9000, triggered at 2021-10-25 23:55:54.780069  
Highest hits @ 2021-10-25 23:55:58.801717  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Traffic recovered - hits = 9000, triggered at 2021-10-25 23:55:54.780069  
Highest hits @ 2021-10-25 23:56:00.810342  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Traffic recovered - hits = 9000, triggered at 2021-10-25 23:55:54.780069  
Highest hits @ 2021-10-25 23:56:02.820359  
bing.fr/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.035626  
bing.it/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.224625  
bing.de/some: hits 10 | total traffic 10000 | last request traffic 1000 @ 2021-10-25 23:55:39.411627  
High traffic generated an alert - hits = 12000, triggered at 2021-10-25 23:55:30.660807  
Traffic recovered - hits = 9000, triggered at 2021-10-25 23:55:54.780069  
```