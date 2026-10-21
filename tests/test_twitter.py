import queue
import time

import pytest
import twitter


def worker(**kwargs):
    return twitter.TwitterThread(queue.Queue(), 'key', 'secret', 'token','secret','station','{dateTime:%H:%M}', '-',twitter.Twitter._DEFAULT_ORDINALS,format_utc=False,**kwargs)


def timestamp(value):
    return int(time.mktime(time.strptime('2026-10-22 '+value,'%Y-%m-%d %H:%M:%S')))


def test_fixed_times_ignore_startup_and_elapsed_interval(monkeypatch):
    posted=[]

    class Client:
        def __init__(self,*args):
            pass

        def update_status(self,status):
            posted.append(status)

    monkeypatch.setattr(twitter,'Twython',Client)
    thread=worker(post_times=['00:00','06:00','12:00','18:00'],post_interval=21600)
    for clock in ['04:31:00','06:00:00','06:00:20','06:35:00','12:00:00','18:00:00']:
        record={'dateTime':timestamp(clock),'usUnits':1}
        if not thread.skip_this_post(record['dateTime']):
            thread.process_record(record,None)
    assert posted==['06:00','12:00','18:00']


@pytest.mark.parametrize('value',['24:00','12:60','wrong','-1:00'])
def test_invalid_times_fail_at_configuration(value):
    with pytest.raises(ValueError):
        worker(post_times=[value])


def test_elapsed_interval_still_works_without_schedule():
    thread=worker(post_interval=21600)
    assert thread.skip_this_post(timestamp('04:31:00')) is False
    assert thread.skip_this_post(timestamp('06:00:00')) is True
    assert thread.skip_this_post(timestamp('10:31:00')) is False
