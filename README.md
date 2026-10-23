# Weather posts to Twitter/X from WeeWX

Format weather observations as text and publish them through Twython's
`update_status` API. The service posts on archive records or LOOP packets, at
an elapsed interval or at fixed local times.

This is the weewx-packages continuation of
[matthewwall/weewx-twitter](https://github.com/matthewwall/weewx-twitter).
[Origin](ORIGIN.md) records the upstream revision; [repair notes](REPAIR_NOTES.md)
describe the maintenance changes.

## Requirements

* An application key and secret plus an OAuth user token and secret. The
  account and application need write access to the API that Twython's
  `update_status` uses. Installing this extension does not grant API access.
  Check the provider's current access conditions.
* The Python package Twython. The extension installer does not install it.
  Activate the virtual environment that runs WeeWX, then run:

  ```sh
  python -m pip install twython
  ```

  For a system installation of WeeWX, use your distribution's Twython package
  for the Python that runs WeeWX.

## Installation

Install `twitter` from the [WeeWX packages catalog](https://github.com/weewx-packages/catalog/blob/main/packages/twitter.md).
The catalog page lists the current release, its WeeWX and Python
requirements, and the install, update and removal commands.

The installer registers `user.twitter.Twitter` as a RESTful service and adds a
`[[Twitter]]` section with placeholder credentials. Replace them as shown
below, restart WeeWX, then check its log after the next eligible record.

## Configuration

```ini
[StdRESTful]
    [[Twitter]]
        app_key = YOUR_APP_KEY
        app_key_secret = YOUR_APP_KEY_SECRET
        oauth_token = YOUR_OAUTH_TOKEN
        oauth_token_secret = YOUR_OAUTH_TOKEN_SECRET
        post_interval = 3600
```

This example posts at most once per hour. Without `post_interval` or
`post_times`, every record produces a post.

| Option | Default | Meaning |
|---|---|---|
| `app_key` | required | Application key. |
| `app_key_secret` | required | Application key secret. |
| `oauth_token` | required | OAuth user token. |
| `oauth_token_secret` | required | OAuth user token secret. |
| `enable` | `true` | Set to `false` to turn the service off. |
| `binding` | `archive` | `archive`, `loop`, or both, comma separated. |
| `station` | `location` from `[Station]` | Station name for the `{station}` placeholder. |
| `format` | see below | Text of each post. |
| `format_None` | `-` | Text for an observation without a value. |
| `ordinals` | `N, NNE, … NNW, N, -` | 18 comma-separated labels for `{windDir:ord}`, from north in 22.5° steps. The last one marks an invalid direction. |
| `format_utc` | `false` | Format `{dateTime}` in UTC instead of local time. |
| `unit_system` | none | `US`, `METRIC` or `METRICWX`. Without it, values keep the units of the record. |
| `post_times` | none | Fixed local posting times, `HH:MM` with two digits each, comma separated. |
| `post_window` | `300` | Seconds after each `post_times` slot in which a record can be posted. |
| `post_interval` | none | Minimum seconds between posts. Ignored when `post_times` is set. |
| `skip_upload` | `false` | Format each post but do not send it. |
| `max_backlog` | unlimited | Queued records kept when posting falls behind. |
| `stale` | none | Skip records older than this many seconds. |
| `log_success` | top-level `log_success`, else `true` | Log each successful post. |
| `log_failure` | top-level `log_failure`, else `true` | Log each failed post. |
| `timeout` | `60` | Seconds to wait for Twitter's server. |
| `max_tries` | `3` | Attempts per record. |
| `retry_wait` | `5` | Seconds between attempts. |

WeeWX logs a warning for any other option in the section and ignores it. An
unknown `unit_system`, a malformed `post_times` entry, or a `post_window` of
zero or less is logged as an error, and the service stays off while WeeWX
keeps running.

### Changing the text

The default format is:

```
{station:%.8s}: Ws: {windSpeed:%.1f}; Wd: {windDir:%03.0f}; Wg: {windGust:%.1f}; oT: {outTemp:%.1f}; oH: {outHumidity:%.2f}; P: {barometer:%.3f}; R: {rain:%.3f}
```

A placeholder is a WeeWX observation name in braces, optionally with a
`%` format after a colon, such as `{outTemp:%.1f}`. Without a format the value
is inserted as it is. `{windDir:ord}` inserts a compass point such as `NNE`.
`{dateTime:%H:%M}` takes a `strftime` format. A placeholder for an observation
that the record does not contain stays in the text unchanged.

### Posting at fixed times

```ini
[StdRESTful]
    [[Twitter]]
        post_times = 00:00, 06:00, 12:00, 18:00
        post_window = 300
```

Records within the window after a slot are posted until one post succeeds. A
window may cross midnight. Each slot is posted at most once per local date, also through a
repeated hour at the end of daylight saving time. Records outside every window
are not posted.

## Limitations

* Fixed times need a record in the window. No timer wakes WeeWX, and missed
  windows are skipped.
* The record of posted slots is kept in memory and resets when WeeWX restarts.
* The service uses Twython's status-update interface. It has no separate API
  v2 writer. Text length, account access and provider limits apply.
* Files in `stash/` are earlier experiments. The installer does not install
  them.
* The tests replace Twython with a local stub. They do not post to a real
  account.

## Development

```sh
python -m pytest -q tests
```

Run it in a Python environment with WeeWX, Twython and pytest installed.

## License

Copyright 2014-2020 Matthew Wall. [GNU GPLv3](license).
