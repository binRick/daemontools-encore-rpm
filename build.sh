#!/usr/bin/env bash
DIR_BASE=$(cd ${BASH_SOURCE[0]%/*} && pwd)
RELEASE_VERSION=$1
if [ "$RELEASE_VERSION" == "" ]; then
	  echo "First argument must be release version to compile"; exit 1
fi

set -e

if [ -f ".daemontools-encore.spec" ]; then
	  unlink .daemontools-encore.spec
fi

cp daemontools-encore.spec.template .daemontools-encore.spec

sed -i "s/__RELEASE_VERSION__/${RELEASE_VERSION}/g" .daemontools-encore.spec

DIR_RPMBUILD=`rpm --eval %{_topdir}`
mkdir -p ${DIR_RPMBUILD}/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

cd ${DIR_RPMBUILD}/SOURCES
rm -rf daemontools-encore; 
git clone https://github.com/bruceg/daemontools-encore  && \
	mv daemontools-encore daemontools-encore-${RELEASE_VERSION} && \
	echo '/usr/bin' > daemontools-encore-${RELEASE_VERSION}/conf-bin && \
	echo '/usr/man' > daemontools-encore-${RELEASE_VERSION}/conf-man && \
	tar -czf ${DIR_RPMBUILD}/SOURCES/daemontools-encore-${RELEASE_VERSION}.tar.gz daemontools-encore-${RELEASE_VERSION} && \
	rm -rf daemontools-encore-${RELEASE_VERSION}
	
#cp -af ${DIR_BASE}/daemontools-encore.tar.gz .
#cp -af ${DIR_BASE}/daemontools-error.h.patch .
#cp -af ${DIR_BASE}/daemontools.conf .
cp -af ${DIR_BASE}/daemontools.service .
cp -af ${DIR_BASE}/svscanboot .
cd - > /dev/null

cd ${DIR_RPMBUILD}/SPECS
cp -af ${DIR_BASE}/.daemontools-encore.spec .
cd - > /dev/null

rpmbuild -ba --clean ${DIR_RPMBUILD}/SPECS/.daemontools-encore.spec

