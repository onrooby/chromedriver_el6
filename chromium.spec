# Based on Tom Callaway's <spot@fedoraproject.org> work

%define chromium_path /opt/chromium-browser
%define flash_version 11.9.900.170

Name:		chromium
Version:	31.0.1650.63
Release:	1%{?dist}
Summary:	A WebKit powered web browser

License:	BSD and LGPLv2+
Group:		Applications/Internet

Patch0:		libudev_extern_c.patch
# http://code.google.com/p/v8/issues/detail?id=2093
Patch1:		v8_gypi_no_strict_aliasing_gcc_46.patch
Patch2:		infobar_unsupported.patch
Patch3:		chromium-gtk-window-utils-gtk-compat.patch
Patch4:		chromium-31.0.1650.48_atk.patch
Patch5:		chromium-31.0.1650.48_gcc_pragma.patch
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=35569
Patch6:		chromium-31.0.1650.48_gcc_workaround.patch
Patch7:		chromium-31.0.1650.57_simplejson.patch
Patch8:		chromedriver-revision.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# From Chromium RHEL use chromium-latest.py --rhel --stable
# http://build.chromium.org/buildbot/official/
Source0:	chromium-%{version}-clean.tar.xz
Source1:	chromium-browser.sh
Source2:	chromium-browser.desktop
# Also, only used if you want to reproduce the clean tarball.
Source6:	clean_ffmpeg.sh
Source7:	chromium-latest.py
Source8:	process_ffmpeg_gyp.py
# https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
Source10:	libpepflashplayer.so.x86_64
Source11:	manifest.json.x86_64
#Source12:	libpdf.so.x86_64
# https://dl.google.com/linux/direct/google-chrome-stable_current_i386.rpm
Source13:	libpepflashplayer.so.i386
Source14:	manifest.json.i386
#Source15:	libpdf.so.i386

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc-c++, bison, flex, gtk2-devel, atk-devel
BuildRequires:	nss-devel >= 3.12.3
BuildRequires:	pciutils-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	cups-devel
BuildRequires:	libudev-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	glibc-devel
BuildRequires:	libXtst-devel
BuildRequires:	fontconfig-devel, GConf2-devel, dbus-devel
BuildRequires:	glib2-devel
BuildRequires:	gperf
BuildRequires:	alsa-lib-devel
BuildRequires:	libusb-devel, expat-devel
BuildRequires:	desktop-file-utils

ExclusiveArch:	%{ix86} arm x86_64

# GTK modules it expects to find for some reason.
Requires:	libcanberra-gtk2%{_isa}

%description
Chromium is an open-source web browser, powered by WebKit.

%prep
%setup -q -n chromium-%{version}

%patch0 -p1 -b .libudev_extern_c
# http://code.google.com/p/v8/issues/detail?id=2093
%patch1 -p1 -b .v8_gypi
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .atk
%patch5 -p1 -b .gcc_pragma
%patch6 -p1 -b .gcc_workaround
%patch7 -p1 -b .simplejson
%patch8 -p1

build/gyp_chromium -f make \
	--depth . \
%ifarch x86_64
	-Dtarget_arch=x64 \
	-Dsystem_libdir=lib64 \
%endif
	-Dgoogle_api_key="AIzaSyBFNqVTy5TNqIg7_p8LT6J-rOvCrP-g2OQ" \
	-Dgoogle_default_client_id="425408526734.apps.googleusercontent.com" \
	-Dgoogle_default_client_secret="lE75DTSrowAf4PCLJwDnZT9h" \
	-Ddisable_glibc=1 \
	-Ddisable_nacl=1 \
	-Ddisable_sse2=1 \
	-Dlinux_link_gnome_keyring=1 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libgps=0 \
	-Dlinux_sandbox_path=%{chromium_path}/chrome-sandbox \
	-Dlinux_sandbox_chrome_path=%{chromium_path}/chromium-browser \
	-Dlinux_strip_binary=1 \
	-Dlinux_use_gold_binary=0 \
	-Dlinux_use_gold_flags=0 \
	-Dlinux_use_libgps=0 \
	-Dlinux_use_tcmalloc=0 \
	-Dmedia_use_libvpx=0 \
	-Dno_strict_aliasing=1 \
	-Dproprietary_codecs=0 \
	-Dremove_webcore_debug_symbols=1 \
	-Duse_gconf=0 \
	-Duse_gnome_keyring=1 \
	-Duse_pulseaudio=1 \
	-Dffmpeg_branding=Chromium \
	-Dlogging_like_official_build=1 \
	-Duse_gio=0 \
	-Dwerror=
#	-Duse_gconf= \
#	-Duse_gio	We don't need GIO on non GNOME 3 desktop
mkdir -p out/Release

%build
export CC="gcc"
export CXX="g++"
export AR="ar"
export RANLIB="ranlib"

make -r %{_smp_mflags} chrome chrome_sandbox chromedriver BUILDTYPE=Release V=1 CC.host="gcc" CFLAGS.host="$PARSED_OPT_FLAGS" CXX.host="g++" CXXFLAGS.host="$PARSED_OPT_FLAGS" LINK.host="g++" LDFLAGS.host="${LDFLAGS}" AR.host="ar"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromium_path}
cp -a %{SOURCE1} %{buildroot}%{chromium_path}/chromium-browser.sh
export BUILDTARGET=`cat /etc/redhat-release`
sed -i "s|@@BUILDTARGET@@|$BUILDTARGET|g" %{buildroot}%{chromium_path}/chromium-browser.sh
export FLASH_VERSION=%{flash_version}
sed -i "s|@@FLASH_VERSION@@|$FLASH_VERSION|g" %{buildroot}%{chromium_path}/chromium-browser.sh
ln -s %{chromium_path}/chromium-browser.sh %{buildroot}%{_bindir}/chromium-browser
mkdir -p %{buildroot}%{_mandir}/man1/

pushd out/Release
cp -a *.pak locales resources %{buildroot}%{chromium_path}
cp -a chrome %{buildroot}%{chromium_path}/chromium-browser
cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
cp -a chromedriver %{buildroot}%{chromium_path}/chromedriver
cp -a chrome.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
mkdir -p %{buildroot}%{chromium_path}/plugins/
cp -a libffmpegsumo.so %{buildroot}%{chromium_path}
popd

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/chromium-browser.png

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE2}

# Bundle PepperFlash and libpdf from Chrome's rpm
mkdir -p %{buildroot}%{chromium_path}/PepperFlash
%ifarch x86_64
	cp -a %{SOURCE10} %{buildroot}%{chromium_path}/PepperFlash/libpepflashplayer.so
	cp -a %{SOURCE11} %{buildroot}%{chromium_path}/PepperFlash/manifest.json
#	cp -a %{SOURCE12} %{buildroot}%{chromium_path}/libpdf.so
%else
	cp -a %{SOURCE13} %{buildroot}%{chromium_path}/PepperFlash/libpepflashplayer.so
	cp -a %{SOURCE14} %{buildroot}%{chromium_path}/PepperFlash/manifest.json
#	cp -a %{SOURCE15} %{buildroot}%{chromium_path}/libpdf.so
%endif

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/chromium-browser
%dir /%{chromium_path}
/%{chromium_path}/*.pak
/%{chromium_path}/chromium-browser
/%{chromium_path}/chromium-browser.sh

%attr(4755, root, root) /%{chromium_path}/chrome-sandbox
%attr(4755, root, root) /%{chromium_path}/chromedriver

/%{chromium_path}/libffmpegsumo.so
/%{chromium_path}/locales/
/%{chromium_path}/plugins/
/%{chromium_path}/resources/
/%{chromium_path}/PepperFlash
%{_mandir}/man1/chromium-browser.*
%{_datadir}/icons/hicolor/256x256/apps/chromium-browser.png
%{_datadir}/applications/*.desktop

#%attr(775, root, root) /%{chromium_path}/libpdf.so
%attr(775, root, root) /%{chromium_path}/PepperFlash/libpepflashplayer.so

%changelog
* Thu Dec 5 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.67-1
- Update to 31.0.1650.63

* Thu Nov 21 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.57-1
- Update to 31.0.1650.57

* Wed Nov 13 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.48-1
- Update to 31.0.1650.48
- Minimal supported RHEL6 version is now RHEL 6.5 due to GTK+

* Fri Oct 25 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.114-1
- Update to 30.0.1599.114
- Hide the infobar with warning that this version of OS is not supported
- Polished the chromium-latest.py

* Thu Oct 17 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.101-1
- Update to 30.0.1599.101
- Minor changes in scripts

* Wed Oct 2 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.66-1
- Update to 30.0.1599.66
- Automated the script for cleaning the proprietary sources from ffmpeg.

* Thu Sep 19 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.76-1
- Update to 29.0.1547.76
- Added script for removing the proprietary sources from ffmpeg. This script is called during cleaning phase of ./chromium-latest --rhel

* Mon Sep 16 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-2
- Compile with Dproprietary_codecs=0 and Dffmpeg_branding=Chromium to disable proprietary codecs (i.e. MP3)

* Mon Sep 9 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-1
- Initial version based on Tom Callaway's <spot@fedoraproject.org> work

