# scrapeclass
eClass web scraper

Requires a config file, `~/.scrapeclass_config.py`, with the following format

```python
logins = {
  ‘firstchild':{ 'login-form-type': 'pwd', 'username': ‘firstECLASSID', 'password': 'firstPASSWORD'},
  ’secondchild':{ 'login-form-type': 'pwd', 'username': 'secondECLASSID', 'password': 'secondPASSWORD'},
  ’thirdchid':{ 'login-form-type': 'pwd', 'username': 'thirdECLASSID', 'password': 'thirdPASSWORD'}
}
```

