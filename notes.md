# gps_parser notes (name pending)

## modules

the app will probably be separated into a few modules. They are:
1. UI
2. general parser
3. log reader
4. com reader

The idea here is that the general parser will contain all the rules of what the binary data means and represents while the log and com modules will determine how the data is obtained. The general parser needs to work with real time data as well as files.

## control design

I'm starting to think the log and com readers should call general parser and send data to it
