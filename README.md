chromedriver_el6
================

In this repo we collect some infos on building current versions of chromium and chromedriver on CentOS 6.

## About

The source rpm provided is based on http://people.centos.org/hughesjr/chromium/6/

All we did was adding chromedriver to the spec, and adding a patch for a failing revision resolution for the chromedriver sources.

## Instructions

#### Get the SRPM for chromium 
```wget http://downloads.onrooby.com/chromium/srpms/chromium-31.0.1650.63-1.el6.src.rpm```

#### Install (**do NOT do this as root!**)
```rpm -ivh chromium-31.0.1650.63-1.el6.src.rpm```

#### Build
```
cd ~/rpmbuild/SPECS
rpmbuild -ba chromium.spec
```

When rpmbuild complains about missing dependencies (mostly devel packages), install them using
```yum install <packagenames>```

## Binaries

We provide pre-built packages, use them on your own risk!

http://downloads.onrooby.com/chromium/rpms/

## TODO

- Split packages into chromium and chromium-chromedriver
