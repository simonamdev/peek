# peek

Get a quick peek into how nginx is performing by parsing the access log and generating some basic statistics.

## Requirements

* Python 3.x
* SQLite3

## Usage

![](https://thumbs.gfycat.com/DetailedDaringAsiaticwildass-size_restricted.gif)

For taking a quick look, which stores the statistics in an in-memory instance of SQLite:

```
python3 peek.py /var/log/nginx/access.log
```

Adjust the /path/to/access.log as necessary.

For persistence of the statistics, add the --persist flag

```
python3 peek.py /var/log/nginx/access.log --persist
```

This currently saves the statistics to the logs.db file in the same directory.

## Known issues

* Currently only works with nginx's default log format
* No check to see if logs.db exists before accessing it

## TODO

* More meaningful error messages when passing incorrect path to access logs
* Flag to specify path to logs database
* Web front end to parse/display the statistics without having to be logged into the same machine

## Contributions

Pull Requests more than welcome! :)

## Licence

MIT Licence