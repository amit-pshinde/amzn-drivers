# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All rights reserved

%define name			efa
%define debug_package		%{nil}

Name:		%{name}
Version:	%{driver_version}
Release:	1%{?dist}
Summary:	%{name} kernel module

Group:		System/Kernel
License:	Dual BSD/GPL
URL:		https://github.com/amzn/amzn-drivers/
Source0:	%{name}-%{version}.tar

Requires:	dkms %kernel_module_package_buildreqs autoconf automake

%define install_path /usr/src/%{name}-%{version}

%description
%{name} kernel module source and DKMS scripts to build the kernel module.

%prep
%setup -n %{name}-%{version} -q

%post
cd %{install_path}
bash ./autogen.sh
dkms add -m %{name} -v %{driver_version}
for kernel in $(/bin/ls /lib/modules); do
	dkms build -m %{name} -v %{driver_version} -k $kernel
	dkms install -m %{name} -v %{driver_version} -k $kernel
done

%preun
dkms remove -m %{name} -v %{driver_version} --all

%build

%install
cd kernel/linux/efa
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{install_path}/config
mkdir -p %{buildroot}%{install_path}/src
install -D -m 644 conf/efa.conf		%{buildroot}/etc/modules-load.d/efa.conf
install -D -m 644 conf/efa-modprobe.conf	%{buildroot}/etc/modprobe.d/efa.conf
install -m 644 conf/dkms.conf		%{buildroot}%{install_path}
install -m 644 README			%{buildroot}%{install_path}
install -m 644 RELEASENOTES.md		%{buildroot}%{install_path}
install -m 644 Makefile.am		%{buildroot}%{install_path}
install -m 644 Makefile.common		%{buildroot}%{install_path}
install -m 644 Makefile.kernel		%{buildroot}%{install_path}
install -m 644 autogen.sh		%{buildroot}%{install_path}
install -m 644 configure.ac		%{buildroot}%{install_path}
install -m 644 config/Makefile		%{buildroot}%{install_path}/config
install -m 644 config/efa.m4		%{buildroot}%{install_path}/config
install -m 644 config/build-linux.m4	%{buildroot}%{install_path}/config
cd src
install -m 644 efa_com.c		%{buildroot}%{install_path}/src
install -m 644 efa_com_cmd.c		%{buildroot}%{install_path}/src
install -m 644 efa_main.c		%{buildroot}%{install_path}/src
install -m 644 efa_sysfs.c		%{buildroot}%{install_path}/src
install -m 644 efa_verbs.c		%{buildroot}%{install_path}/src
install -m 644 efa_gdr.c		%{buildroot}%{install_path}/src
install -m 644 efa_gdr.h		%{buildroot}%{install_path}/src
install -m 644 efa-abi.h 		%{buildroot}%{install_path}/src
install -m 644 efa_admin_cmds_defs.h 	%{buildroot}%{install_path}/src
install -m 644 efa_admin_defs.h 	%{buildroot}%{install_path}/src
install -m 644 efa_com_cmd.h		%{buildroot}%{install_path}/src
install -m 644 efa_com.h		%{buildroot}%{install_path}/src
install -m 644 efa_common_defs.h	%{buildroot}%{install_path}/src
install -m 644 efa.h			%{buildroot}%{install_path}/src
install -m 644 efa_regs_defs.h		%{buildroot}%{install_path}/src
install -m 644 efa_sysfs.h		%{buildroot}%{install_path}/src
install -m 644 kcompat.h		%{buildroot}%{install_path}/src
install -m 644 Makefile.am		%{buildroot}%{install_path}/src

%files
%{install_path}
/etc/modules-load.d/efa.conf
/etc/modprobe.d/efa.conf

%changelog
* Wed Feb 26 2020 Gal Pressman <galpress@amazon.com> - 1.6.0
- Add NVIDIA GPUDirect RDMA support
- Add a configure script to the compilation process and use it to test for kernel funcionality
- Change directory structure, the source files are now located under src/
- Fix compilation on certain kernels of SuSE15.1
- Backport changes from upstream kernel

* Thu Jan 02 2020 Gal Pressman <galpress@amazon.com> - 1.5.1
- Fix SuSE ioctl flow backport

* Wed Dec 11 2019 Gal Pressman <galpress@amazon.com> - 1.5.0
- RDMA read support
- Make ib_uverbs a soft dependency
- Fix ioctl flows on older kernels
- SuSE 15.1 support

* Fri Sep 20 2019 Gal Pressman <galpress@amazon.com> - 1.4.1
- Fix Incorrect error print
- Add support for CentOS 7.7

* Thu Sep 5 2019 Gal Pressman <galpress@amazon.com> - 1.4.0
- Expose device statistics
- Rate limit admin queue error prints
- Properly assign err variable on everbs device creation failure

* Thu Aug 8 2019 Gal Pressman <galpress@amazon.com> - 1.3.1
- Fix build issue in debian/rules file
- Fix kcompat issue (usage before include)

* Sun Jul 7 2019 Gal Pressman <galpress@amazon.com> - 1.3.0
- Align to the driver that was merged upstream
- Fix a bug where failed functions would return success return value
- Fix modify QP udata check backport
- Fix locking issues in mmap flow
- Add Debian packaging files

* Tue May 7 2019 Jie Zhang <zhngaj@amazon.com> - 0.9.2
- Add a separate configuration file to load ib_uverbs as a soft dependency module
  on non-systemd based systems

* Tue Apr 2 2019 Robert Wespetal <wesper@amazon.com> - 0.9.1
- Update EFA post install script to install module for all kernels

* Fri Mar 8 2019 Robert Wespetal <wesper@amazon.com> - 0.9.0
- initial build for RHEL
