# Weather posts to Twitter/X from WeeWX

Format weather observations as text and publish them through Twython's
`update_status` API. The service supports archive or LOOP events and optional
fixed local posting times.

This is the weewx-packages continuation, release **0.16.1**.
[Origin](ORIGIN.md) records the upstream revision; [repair notes](REPAIR_NOTES.md)
describe the maintenance changes.

The catalog archive targets WeeWX `>=5.5.2,<5.7` and Python `>=3.10,<3.15`.

## Requirements

Install Twython in the Python environment running WeeWX. For a WeeWX virtual
environment:

```sh
python -m pip install twython
```

You need an application key and secret plus an OAuth user token and secret.
The account and application must have write access to the API used by
Twython's `update_status`. Check the provider's current access conditions;
installing this extension does not grant API access.

## Install

Use `weectl` from the Python environment running WeeWX. With stock WeeWX 5,
install the published archive:

```sh
weectl extension install https://github.com/weewx-packages/weewx-twitter/releases/download/v0.16.1/weewx-twitter-0.16.1.tar.gz --config /path/to/weewx.conf
```

Replace `/path/to/weewx.conf` with your station configuration. You can also
download that URL and pass the local archive to the same command. Use elevated
permissions only when your station files require them.

## Configure posts

```ini
[StdRESTful]
    [[Twitter]]
        app_key = YOUR_APP_KEY
        app_key_secret = YOUR_APP_KEY_SECRET
        oauth_token = YOUR_OAUTH_TOKEN
        oauth_token_secret = YOUR_OAUTH_TOKEN_SECRET
        post_interval = 3600
```

The installer registers `user.twitter.Twitter`. Restart WeeWX yourself and
check its log after an eligible archive record. This example limits posts to
one per hour. Without `post_interval` or `post_times`, each arriving record can
produce a post.

## Format and schedule

The default text includes the station name and common weather readings in
archive units. Set `unit_system` to `US`, `METRIC` or `METRICWX` to convert them.
The `format` setting uses placeholders such as `{outTemp:%.1f}`,
`{windDir:ord}` and `{dateTime:%H:%M}`. `format_None` substitutes for null values;
`format_utc = true` formats timestamps in UTC. See
[bin/user/twitter.py](bin/user/twitter.py) for the default format and options.

For fixed local times, add:

```ini
[StdRESTful]
    [[Twitter]]
        post_times = 00:00, 06:00, 12:00, 18:00
        post_window = 300
```

`post_times` takes precedence over `post_interval`. The first record within the
window after a slot is eligible. Successful posts occur once per local date
and slot while the service runs. Missed windows are skipped; slot history is
in memory and resets on restart. No timer wakes WeeWX to collect readings.
`binding = loop` selects LOOP events; the default is `archive`.

The implementation uses Twython's status-update interface and has no separate
API v2 writer. Text length, account access and provider limits still apply.
Files in `stash/` are earlier experiments, not installed services.

Copyright 2014-2020 Matthew Wall. [GNU GPLv3](license).
