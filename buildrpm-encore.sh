#!/usr/bin/env bash
DIR_BASE=$(cd ${BASH_SOURCE[0]%/*} && pwd)
set -e

DIR_RPMBUILD=`rpm --eval %{_topdir}`
mkdir -p ${DIR_RPMBUILD}/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

cd ${DIR_RPMBUILD}/SOURCES
rm -rf daemontools-encore; 
git clone https://github.com/bruceg/daemontools-encore  && \
	mv daemontools-encore daemontools-encore-1.11 && \
	echo '/usr/bin' > daemontools-encore-1.11/conf-bin && \
	echo '/usr/man' > daemontools-encore-1.11/conf-man && \
	tar -czf ${DIR_RPMBUILD}/SOURCES/daemontools-encore-1.11.tar.gz daemontools-encore-1.11 && \
	rm -rf daemontools-encore-1.11
	
#cp -af ${DIR_BASE}/daemontools-encore.tar.gz .
#cp -af ${DIR_BASE}/daemontools-error.h.patch .
cp -af ${DIR_BASE}/daemontools.conf .
cp -af ${DIR_BASE}/daemontools.service .
cp -af ${DIR_BASE}/svscanboot .
cd - > /dev/null

cd ${DIR_RPMBUILD}/SPECS
cp -af ${DIR_BASE}/daemontools-encore.spec .
cd - > /dev/null

rpmbuild -ba --clean ${DIR_RPMBUILD}/SPECS/daemontools-encore.spec

