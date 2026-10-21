twitter - weewx extension that sends data to Twitter
Copyright 2014-2020 Matthew Wall
Distributed under the terms of the GNU Public License (GPLv3)

===============================================================================
Pre-requisites

Install the twitter python bindings

For python3:

sudo pip3 install twython

For python2:

sudo pip install twython


===============================================================================
Installation instructions

1) download

wget -O weewx-twitter.zip https://github.com/weewx-packages/weewx-twitter/archive/master.zip

2) run the installer:

wee_extension --install weewx-twitter.zip

3) modify weewx.conf:

[StdRESTful]
    [[Twitter]]
        app_key = APP_KEY
        app_key_secret = APP_KEY_SECRET
        oauth_token = OAUTH_TOKEN
        oauth_token_secret = OAUTH_TOKEN_SECRET

4) restart weewx

sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start


===============================================================================
Options

For configuration options and details, see the comments in twitter.py

Fixed local posting times

[StdRESTful]
    [[Twitter]]
        post_times = 00:00, 06:00, 12:00, 18:00

The first record within post_window seconds after each local time is posted.
The default window is 300 seconds. Successful posts occur at most once per
local date and slot while the service runs. Missing windows are skipped.
post_times takes precedence over post_interval. With no post_times, the
existing elapsed post_interval behaviour applies. The service needs a record
at the scheduled time; it does not wake the station to collect a sample.

Modified 2026-10-22 by weewx-packages.
