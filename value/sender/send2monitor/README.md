# Send value to the MONITOR™

## prerequirements
[pip install error-counter](https://pypi.org/project/error-counter/)

## settings
send2monitor.ini file on the same directory of this module is used to solve settings.

### settings items.
- [valueid]
  - value : value_id of MONITOR™ related to value. For exameple, co2=abcdefg

- [server]
  - url: MONITOR™ server url. Basically, no need to change.

- [error_recovery]
  - recover_on:  true or false, indicate do error recovery or not.
  - counterfile: file path to use error count

