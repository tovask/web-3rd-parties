# privchk - Privacy checks on websites

---

### Calculate 3rd party requests count on the top websites
Sample result:

top level url | total requests count | third party requests
---- | :---: | :---:
https://www.microsoft.com/en-us/ | 139 | 122
https://www.youtube.com/ | 117 | 83
https://www.facebook.com/ | 64 | 60
https://www.netflix.com/ | 57 | 47
https://www.linkedin.com/ | 45 | 39
https://twitter.com/ | 18 | 16
http://www.baidu.com/ | 19 | 12
https://www.google.com/?gws_rd=ssl | 15 | 7
https://www.instagram.com/ | 28 | 7
http://baidu.com/ | 2 | 1
https://www.wikipedia.org/ | 7 | 0

---

### Show where the webservers located (in which country)
(The measurements performed on the top 500 Hungarian websites, but this is just a matter of the list used.)  
Using [ipapi](https://github.com/ipapi-co/ipapi-python) for geolocation,  
[sqlite3](https://docs.python.org/3/library/sqlite3.html) for store the data.

---

### Automatically find (and hide) GDPR consent dialog
Find the close button of the dialog, with a small javascript code.  
(The keywords have been optimized for Hungarian sites, but this can be easily changed to any arbitrary localization.)

---

Moreover, [this gist](https://gist.github.com/tovask/f8ccd573a950fc47e3aaa311a8f012b9) analyze block lists changes based on [PyFunceble](https://github.com/funilrys/PyFunceble) Github repositories.
