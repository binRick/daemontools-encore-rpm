%define _name	daemontools-encore
%define _ver	1.11
%define _dist	%(sh /usr/lib/rpm/redhat/dist.sh)
%define _rel	1%{?_dist}
%global debug_package %{nil}


Name:		%{_name}
Version:	%{_ver}
Release:	%{_rel}
Summary:	Service Monitoring and Logging Utilities
Group:		Unspecified
License:	Public Domain
URL:		http://cr.yp.to/daemontools.html
Source0:	daemontools-encore-1.11.tar.gz
#Patch0:		daemontools-error.h.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root


%description
daemontools is a collection of tools for managing UNIX services.

supervise monitors a service. It starts the service and restarts the service
if it dies. Setting up a new service is easy: all supervise needs is a directory
with a run script that runs the service.

multilog saves error messages to one or more logs. It optionally timestamps each
line and, for each log, includes or excludes lines matching specified patterns.
It automatically rotates logs to limit the amount of disk space used.
If the disk fills up, it pauses and tries again, without losing any data.


%prep
%setup -q -n %{_name}-%{_ver}
#%patch0 -p0


%build
./makedist
./makemake
make
find


%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
for x in envdir envini envuidgid fghack multilog pgrphack readproctitle setlock setuidgid setuser softlimit supervise svc svok svscan svscanboot svstat svup tai64n tai64nlocal envini setuser svup
do
cp -fp $x ${RPM_BUILD_ROOT}/usr/bin
done
#cp -fp ${RPM_SOURCE_DIR}/svscanboot ${RPM_BUILD_ROOT}/usr/bin
#%if 0%{?rhel} >= 7 || 0%{?fedora} >= 23
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system
cp -p ${RPM_SOURCE_DIR}/daemontools.service ${RPM_BUILD_ROOT}/usr/lib/systemd/system
#%endif
#%if 0%{?el6}
#mkdir -p ${RPM_BUILD_ROOT}/etc/init
#cp -p ${RPM_SOURCE_DIR}/daemontools.conf ${RPM_BUILD_ROOT}/etc/init
#%endif
#find %{buildroot} -type f | sed 's|^%{buildroot}||' > filelist
#cat filelist

%clean
rm -rf ${RPM_BUILD_ROOT}


%post
[ -d /service ] || mkdir /service

%if 0%{?el6}
initctl reload-configuration
%endif
%if 0%{?el5} || 0%{?el4}
echo 'SV:123456:respawn:/usr/bin/svscanboot' >> /etc/inittab
%endif


%preun
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 23
systemctl stop daemontools.service
systemctl disable daemontools.service 2> /dev/null
%endif
%if 0%{?el6}
initctl stop daemontools > /dev/null 2>&1 ||:
%endif
%if 0%{?el5} || 0%{?el4}
pkill svscan ||:
pkill svscanboot ||:
%endif


%postun
%if 0%{?el6}
initctl reload-configuration
%endif
%if 0%{?el5} || 0%{?el4}
sed -i '/svscanboot/d' /etc/inittab
%endif

rmdir /service 2> /dev/null ||:


#%files -f filelist

%files
%attr(0755,root,root) /usr/bin/envini
%attr(0755,root,root) /usr/bin/setuser
%attr(0755,root,root) /usr/bin/svup
%attr(0755,root,root) /usr/bin/envdir
%attr(0755,root,root) /usr/bin/envuidgid
%attr(0755,root,root) /usr/bin/fghack
%attr(0755,root,root) /usr/bin/multilog
%attr(0755,root,root) /usr/bin/pgrphack
%attr(0755,root,root) /usr/bin/readproctitle
%attr(0755,root,root) /usr/bin/setlock
%attr(0755,root,root) /usr/bin/setuidgid
%attr(0755,root,root) /usr/bin/softlimit
%attr(0755,root,root) /usr/bin/supervise
%attr(0755,root,root) /usr/bin/svc
%attr(0755,root,root) /usr/bin/svok
%attr(0755,root,root) /usr/bin/svscan
%attr(0555,root,root) /usr/bin/svscanboot
%attr(0755,root,root) /usr/bin/svstat
%attr(0755,root,root) /usr/bin/tai64n
%attr(0755,root,root) /usr/bin/tai64nlocal
%attr(0644,root,root) /usr/lib/systemd/system/daemontools.service


%changelog
* Sun Jul 20 2014 teru <teru@kteru.net>
- Added startup script for el7
* Fri Sep 16 2011 teru <teru@kteru.net>
- Added startup script for el6
* Wed Mar 2 2011 teru <teru@kteru.net>
- Initial version

