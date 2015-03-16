# connlist
Output a list of connections based on "Built Connection" firewall log messages.

When searching through firewall logs, it is often hard to get a good overview of the traffic flow as the number of messages increase. This connlist script summarizes all connections it sees and outputs a easy-to-read table of connection information.

## Dependencies

The 'fw-regex' library (another one of my repositories) is used to extract interesting data from log lines. It is added as a submodule of this repo.

Follow these steps to update the dependency to the newest version:
```cd lib/fw-regex
git pull
```

## Usage

Simply pipe firewall log lines to `connlist.py` to get them summarized:

```
$ zfgrep 80.65.59.162 test/fw.log-20150202.gz | ./connlist.py
 COUNT PROTO  FROM IP         TO IP          PORT  FIRST SEEN           LAST SEEN
    18  TCP   228.106.58.87     80.65.59.162 443   2015-02-02 07:51:09  2015-02-02 07:51:41
     7  TCP   173.238.13.22     80.65.59.162 443   2015-02-02 07:49:49  2015-02-02 07:49:50
    45  TCP   110.141.24.75     80.65.59.162 443   2015-02-01 08:38:38  2015-02-02 07:14:16
     3  TCP   173.238.13.27     80.65.59.162 443   2015-02-02 07:30:05  2015-02-02 07:30:09
    23  TCP  213.126.22.155     80.65.59.162 443   2015-02-02 07:45:13  2015-02-02 07:52:04
    29  TCP   173.238.13.25     80.65.59.162 443   2015-02-02 07:09:08  2015-02-02 07:50:21
    29  TCP  134.70.126.189     80.65.59.162 443   2015-02-02 07:28:43  2015-02-02 07:35:51
    28  TCP   173.238.13.30     80.65.59.162 443   2015-02-01 11:17:51  2015-02-01 14:12:58
     7  TCP   173.238.13.86     80.65.59.162 443   2015-02-02 07:51:12  2015-02-02 07:51:16
     6  TCP   228.106.58.74     80.65.59.162 443   2015-02-02 07:24:30  2015-02-02 07:24:30
    22  TCP  248.126.111.26     80.65.59.162 443   2015-02-02 06:52:33  2015-02-02 06:59:58
    18  TCP   173.238.13.43     80.65.59.162 443   2015-02-02 06:44:17  2015-02-02 07:41:32
     6  TCP   228.106.58.89     80.65.59.162 443   2015-02-02 07:26:17  2015-02-02 07:29:34
     9  TCP   213.126.22.56     80.65.59.162 443   2015-02-02 07:36:35  2015-02-02 07:50:34
    14  TCP   110.141.24.74     80.65.59.162 443   2015-02-01 08:19:11  2015-02-01 16:55:54
     2  TCP   173.238.13.88     80.65.59.162 443   2015-02-02 07:14:41  2015-02-02 07:41:30
   113  TCP  110.141.24.221     80.65.59.162 443   2015-02-01 08:03:01  2015-02-01 13:34:21
     9  TCP   173.238.13.89     80.65.59.162 443   2015-02-02 07:38:08  2015-02-02 07:39:55
     7  TCP   228.106.58.12     80.65.59.162 443   2015-02-02 07:37:38  2015-02-02 07:37:39
     4  TCP  134.70.126.189     80.65.59.162 80    2015-02-02 07:28:43  2015-02-02 07:35:13
     1  TCP   228.106.58.87     80.65.59.162 80    2015-02-02 07:51:09  2015-02-02 07:51:09
```

Here I searched for a specific IP address to see what traffic the firewall has seen to or from that address. Instead of having to look through 805 firewall log lines I can quickly check the short table to find out what clients created the most sessions, what time range each client was active and what port numbers each client contacted on the server.

Instead of searching for an IP address I could just as easily have searched for a port number, to get a table of all client+server pairs communicating using that port. As you can see from the output above the script reads log lines from standard input, suitable for piping data to. It can also be used as a Hadoop Streaming reducer if the amount of log data is big enough to warrant a Hadoop Streaming job.


