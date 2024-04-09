%define  __python /usr/bin/python3

Name:       migration-tools
Version:    1.0.1
Release:    3
License:    MulanPSL-2.0
Summary:    A tool to help users migrate the Centos system to the UOS system and openEuler system
Source0:    migration-tools.tar.gz
Source1:    requires.tar.gz
Source2:    xlwt-1.3.0-py2.py3-none-any.whl
# patches
Patch0:     0001-use-kill-not-kill-INT-when-stop-service.patch

# CVE patches: >= 100
Patch100:   100-CVE-2024-24892.patch

BuildArch:  noarch
%description
UOS Migration Software

%if 0%{?rhel} >= 7
%package -n migration-tools-agent
Summary:        migration-tools-agent
License:        MulanPSL-2.0
Requires:       dnf
Requires:       libabigail
Requires:       python3
Requires:       python3-flask
Requires:       python3-paramiko
Requires:       python3-requests
Requires:       python3-xlrd
Requires:       python3-xlwt
Requires:       openssl
Requires:       rsync
Requires:       yum-utils

%description -n migration-tools-agent
Migration software agent side
%endif

%package -n migration-tools-server
Summary: 	migration-tools-server
License:	MulanPSL-2.0
Requires:	python3
Requires:	python3-pip
Requires:	sshpass
Requires:	python3-paramiko
Requires:	python3-flask
Requires:	python3-requests

%description -n migration-tools-server
Migration software server side


%prep
%setup -c

%patch 0 -p1
%patch 100 -p1

%if 0%{?openEuler}
cp -f %SOURCE1 agent-requires/
cp -f %SOURCE2 agent-requires/
%endif

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/lib/migration-tools-server
mkdir -p $RPM_BUILD_ROOT/var/tmp/uos-migration
mkdir -p $RPM_BUILD_ROOT/etc/migration-tools
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

cp -r * $RPM_BUILD_ROOT/usr/lib/migration-tools-server/

%if 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT/usr/lib/migration-tools-agent
cp -r * $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/
%{__cp} -r $RPM_BUILD_ROOT/usr/lib/migration-tools-server/server/migration-tools-agent.service $RPM_BUILD_ROOT%{_unitdir}
%endif

# Install server config
%{__cp} -r $RPM_BUILD_ROOT/usr/lib/migration-tools-server/server/migration-tools.conf $RPM_BUILD_ROOT/etc/migration-tools
%{__cp} -r $RPM_BUILD_ROOT/usr/lib/migration-tools-server/server/migration-tools-server.service $RPM_BUILD_ROOT%{_unitdir}

%posttrans
%{_bindir}/systemctl daemon-reload

%post -n migration-tools-server
pip3 install /usr/lib/migration-tools-server/agent-requires/xlwt-1.3.0-py2.py3-none-any.whl --no-cache-dir
chmod +x /usr/lib/migration-tools-server/server/start_webview.sh
ln -sf /usr/lib/migration-tools-server/server/start_webview.sh /usr/bin/migration-tools

%preun -n migration-tools-server
if [ $1 = 0 ];then
    systemctl stop migration-tools-server.service
fi

%postun -n migration-tools-server
rm -rf /usr/bin/migration-tools

%files -n migration-tools-server
/etc/migration-tools
/usr/lib/migration-tools-server
%{_unitdir}/migration-tools-server.service

%if 0%{?rhel} >= 7
%files -n migration-tools-agent
/etc/migration-tools
/usr/lib/migration-tools-agent
%{_unitdir}/migration-tools-agent.service
%endif

%changelog
* Mon Mar 18 2024 lixin <lixinb@uniontech.com> - 1.0.1-3
- fix stop service display failed
- update spec

* Mon Mar 11 2024 lixin <lixinb@uniontech.com> - 1.0.1-2
- fix : CVE-2024-24892
- use paramiko instead of sshpass to export migration log
- and data

* Tue Mar 05 2024 lixin <lixinb@uniontech.com> - 1.0.1-1
- Supports migrations to OpenEuler system using the web-based interface.

* Wed Sep 06 2023 lixin <lixinb@uniontech.com> - 1.0.0-4
- fix: fix uefi boot failed
- fix: modify grub rules to match NIC name after migration

* Tue Aug 22 2023 lixin <lixinb@uniontech.com> - 1.0.0-3
- feat: add aarch64 agent package

* Mon Aug 21 2023 lixin <lixinb@uniontech.com> - 1.0.0-2
- fix export log and migration report error
- fix no migration detail error

* Wed Aug 16 2023 lixin <lixinb@uniontech.com> - 1.0.0-1
- init
