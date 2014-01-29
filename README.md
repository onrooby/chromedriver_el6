chromedriver_el6
================

In this repo we collect some infos on building current versions of chromium and chromedriver on CentOS 6.

## About

On CentOS 6, you get the following error when trying to start chromedriver:

```
/lib64/libc.so.6: version `GLIBC_2.14' not found (required by ./chromedriver)
./chromedriver: /lib64/libc.so.6: version `GLIBC_2.15' not found (required by ./chromedriver)
./chromedriver: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.15' not found (required by ./chromedriver)
```

The source rpm provided is based on http://people.centos.org/hughesjr/chromium/6/

All we did was adding chromedriver to the spec, and adding a patch for a failing revision resolution for the chromedriver sources.

## Current Versions

| Program       | Version       |
|---------------|---------------|
| ChromeDriver  | v2.3          |
| Chromium      | 31.0.1650.63  |

## Instructions

**Do NOT do this as root! You might damage your system!**
RPM building will take place in ```~/rpmbuild```.

#### Get the SRPM for chromium 
```wget http://downloads.onrooby.com/chromium/srpms/chromium-31.0.1650.63-1.el6.src.rpm```

#### Install (as normal user)
```rpm -ivh chromium-31.0.1650.63-1.el6.src.rpm```

#### Build
```
cd ~/rpmbuild/SPECS
rpmbuild -ba chromium.spec
```

When rpmbuild complains about missing dependencies (mostly devel packages), install them using
```yum install <packagenames>```

## Binaries

We provide pre-built packages. Use at your own risk!

http://downloads.onrooby.com/chromium/rpms/

## TODO

- Split packages into chromium and chromium-chromedriver
