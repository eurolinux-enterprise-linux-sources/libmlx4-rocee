Name: libmlx4-rocee
Version: 1.0.5
Release: 1%{?dist}
Summary: Mellanox ConnectX InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/mlx4/libmlx4-%{version}.tar.gz
Source1: libmlx4-modprobe.conf
Source2: libmlx4-mlx4.conf
Source3: libmlx4-setup.sh
Source4: libmlx4-dracut-check.sh
Source5: libmlx4-dracut-install.sh
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: libmlx4 = %{version}
Provides: libmlx4-devel = %{version}
Provides: libmlx4-rocee-devel = %{version}-%{release}
Obsoletes: libmlx4 < 1.0.6
Obsoletes: libmlx4-devel < 1.0.6
BuildRequires: libibverbs-devel > 1.1.5
BuildRequires: valgrind-devel
ExcludeArch: s390 s390x
Requires: dracut
%global dracutlibdir %{_datadir}/dracut

%description
libmlx4 provides a device-specific userspace driver for Mellanox
ConnectX HCAs for use with the libibverbs library.

%package static
Summary: Static version of the libmlx4 driver
Group: System Environment/Libraries
Provides: libmlx4-static = %{version}
Obsoletes: libmlx4-static < 1.0.6
Provides: libmlx4-devel-static = %{version}-%{release}
Obsoletes: libmlx4-devel-static < 1.0.6
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmlx4 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q -n libmlx4-%{version}

%build
%configure --with-valgrind
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/modprobe.d/libmlx4.conf
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rdma/mlx4.conf
install -D -m 755 %{SOURCE3} %{buildroot}%{_libexecdir}/setup-mlx4.sh
install -D -m 755 %{SOURCE4} %{buildroot}%{dracutlibdir}/modules.d/90-libmlx4/check
install -D -m 755 %{SOURCE5} %{buildroot}%{dracutlibdir}/modules.d/90-libmlx4/install
# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/libmlx4.{la,so}

%files
%defattr(-,root,root,-)
%{_libdir}/libmlx4-rdmav2.so
%{_sysconfdir}/libibverbs.d/mlx4.driver
%{_sysconfdir}/modprobe.d/libmlx4.conf
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%{_libexecdir}/setup-mlx4.sh
%{dracutlibdir}/modules.d/90-libmlx4
%doc AUTHORS COPYING README

%files static
%defattr(-,root,root,-)
%{_libdir}/libmlx4.a

%changelog
* Mon Oct 28 2013 Doug Ledford <dledford@redhat.com> - 1.0.5-1
- Update to match rhel-6.5 libmlx4 package
- Related: bz879191

* Tue Oct 23 2012 Doug Ledford <dledford@redhat.com> - 1.0.4-1
- Update to latest upstream version
- Related: bz756396

* Wed Mar 21 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-5
- Fix modprobe file so it can't render a machine unbootable if run against
  an older kernel.
- Resolves: bz805129

* Wed Mar 14 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-4
- Update mlx4 modprobe file to indicate that the HPN channel is installed
- Related: bz753004

* Tue Jan 31 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-3
- Update to the version of rocee that landed upstream (now known as iboe)
- Related: bz756399

* Wed Aug 03 2011 Doug Ledford <dledford@redhat.com> - 1.0.2-2
- Fix the fix to the modprobe file
- Related: bz725016

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Update to latest upstream version
- Drop 6 patches rolled into latest upstream version
- Drop ifnarch ia64 around valgrind usage as we don't build for ia64
- Fix broken libmlx4-modprobe.conf file
- Related: bz725016

* Wed Jun 16 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-8
- Add RoCEE support
- Related: bz603807

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-5
- Update upstream URLs
- Related: bz543948

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-4
- Don't try to build on s390(x) as the hardware doesn't exist there

* Sat Dec 05 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-3
- Tweak the provides and obsoletes a little bit to make sure we only pull in
  the -static package to replace past -devel-static packages, and not past
  -devel packages.

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-2
- Merge various bits from Red Hat package into Fedora package

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-1
- Update to latest upstream release
- Add pseudo provides of libibverbs-driver
- Update buildrequires for libibverbs API change

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 27 2008 Roland Dreier <rdreier@cisco.com> - 1.0-2
- Spec file cleanups, based on Fedora review: don't mark
  libmlx4.driver as a config file, since it is not user modifiable,
  and change the name of the -devel-static package to plain -devel,
  since it would be empty without the static library.

* Sun Dec  9 2007 Roland Dreier <rdreier@cisco.com> - 1.0-1
- New upstream release

* Fri Apr  6 2007 Roland Dreier <rdreier@cisco.com> - 1.0-0.1.rc1
- Initial Fedora spec file
