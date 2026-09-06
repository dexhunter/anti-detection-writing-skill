First check whether the missing messages are absent from `caplog` or only from the failed test's captured-log section. Those use separate handlers. A local pytest 9.0.2 check with `log_level = INFO` captured DEBUG records after `caplog.set_level(logging.DEBUG)`, while the report handler remained at INFO.

```python
def test_debug(caplog):
    caplog.set_level(logging.DEBUG)
    logging.debug("debug marker")
    assert "debug marker" in caplog.text
```

The [fixture implementation](https://github.com/pytest-dev/pytest/blob/9.0.2/src/_pytest/logging.py) changes both the selected logger's level and the fixture's capture-handler level. It does not imply that the separate report or live-log handler changes too.

If the assertion passes, the fixture is capturing the message despite what the report displays. If it fails only in your project, check logger levels, filters, root-handler replacement and propagation. Targeting a named logger does not by itself undo `propagate = False`; its records still need to reach the capture handler. This isolated check does not reproduce your project's logging configuration or establish a regression there.
