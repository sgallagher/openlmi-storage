# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           cura-storage
Version:        0.1
Release:        1%{?dist}
Summary:        CIM providers for storage management

License:        GPLv2+
URL:            http://fedorahosted.org/cura
Source0:        cura-storage-0.1.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       cmpi-bindings-pywbem
Requires:       anaconda
# For Linux_ComputerSystem:
Requires:       sblim-cmpi-base

%description
The cura-storage package contains CMPI providers for management of storage using
Common Information Managemen (CIM) protocol.

The providers can be registered in any CMPI-aware CIMOM, both OpenPegasus and
SFCB were tested.

%prep
%setup -q

%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

install -m 755 -d $RPM_BUILD_ROOT/%{_datadir}/cura-storage
install -m 644 mof/* $RPM_BUILD_ROOT/%{_datadir}/cura-storage/

%files
%doc README COPYING
%{python_sitelib}/*
%{_datadir}/cura-storage

%changelog
* Tue Jul 24 2012 Jan Safranek <jsafrane@redhat.com> - 0.1-1
- Package created.
