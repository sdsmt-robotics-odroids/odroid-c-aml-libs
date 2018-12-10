%global commit 820b12a9440fb50744f677e3d6b8b650c8e3a9fd
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           odroid-c-aml-libs
Version:        2015.01.09
Release:        3%{?dist}
Summary:        ODROID-C Amlogic Libraries

Group:          System Environment/Libraries
License:        Proprietary
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-c1
Source0:        https://github.com/mdrjr/c1_aml_libs/archive/%{commit}/c1_aml_libs-%{commit}.tar.gz
Source1:        99-amlogic.rules
Patch0:         %{name}-2015.01.09-makefile_cleanups.patch
Patch1:         %{name}-2015.01.09-relative-includes.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  gcc

%package devel
Summary:        ODROID-C Amlogic Headers
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       alsa-lib-devel

%description
ODROID-C Amlogic Libraries

%description devel
ODROID-C Amlogic Headers

%prep
%setup -qn c1_aml_libs-%{commit}
%patch0 -p1
%patch1 -p1

find . -name *.so -o -name *~ -o -name *.o | xargs rm -f

%build
CFLAGS="${CFLAGS:-%optflags}" make %{?_smp_mflags}

%install
install -d %{buildroot}%{_includedir}/{amports,cutils,ppmgr,amcodec,amadec,amavutils}/
install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_prefix}/lib/udev/rules.d/

install -p -m755 amadec/libamadec.so amavutils/libamavutils.so amcodec/libamcodec.so %{buildroot}%{_libdir}/
install -p -m644 amadec/{,include/}*.h %{buildroot}%{_includedir}/amadec/
install -p -m644 amavutils/include/*.h %{buildroot}%{_includedir}/amavutils/
install -p -m644 amavutils/include/cutils/*.h %{buildroot}%{_includedir}/cutils/
install -p -m644 amcodec/include/*.h %{buildroot}%{_includedir}/amcodec/
install -p -m644 amcodec/include/amports/*.h %{buildroot}%{_includedir}/amports/
install -p -m644 amcodec/include/ppmgr/*.h %{buildroot}%{_includedir}/ppmgr/
install -p -m644 %{SOURCE1} %{buildroot}%{_prefix}/lib/udev/rules.d/99-amlogic.rules

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so*
%{_prefix}/lib/udev/rules.d/99-amlogic.rules

%files devel
%{_includedir}/amports/
%{_includedir}/cutils/
%{_includedir}/ppmgr/
%{_includedir}/amcodec/
%{_includedir}/amadec/
%{_includedir}/amavutils/

%changelog
* Mon Dec 10 2018 Scott K Logan <logans@cottsay.net> - 2015.01.09-3
- Add BuildRequires: gcc

* Mon Oct 17 2016 Scott K Logan <logans@cottsay.net> - 2015.01.09-2
- Add patch from Kodi repository

* Sun May 10 2015 Scott K Logan <logans@cottsay.net> - 2015.01.09-1
- Initial package
