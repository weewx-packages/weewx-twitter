# Repair validation

Version 0.16.0. Original repository and revision are in ORIGIN.md.

* https://github.com/matthewwall/weewx-twitter/issues/4: post_times HH:MM with bounded window and once-per-slot success; takes precedence over elapsed interval. Test starts at 04:31 and posts at 06:00,12:00,18:00 without duplicates. Public Twitter account/API entitlement not tested; no records means no scheduled send.

Tests run under WeeWX 4.10.2/5.1.0 on Python 3.10 and WeeWX 5.5.2 on Python 3.14. Local receivers and isolated install directories avoid live station changes. The tests do not establish individual external account permissions.
