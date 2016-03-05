%global scl_name_prefix sclo-
%global scl_name_base subversion
%global scl_name_version 19

%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}
%scl_package %scl

# Do not produce empty debuginfo package.
%global debug_package %{nil}

%global install_scl 1

Summary: Package that installs %scl
Name: %scl_name
# should match the RHSCL version
Version: 1.0
Release: 1%{?dist}
Group: Applications/File
Source0: README
Source1: LICENSE
License: GPLv2+
Requires: scl-utils
%if 0%{?install_scl}
Requires: %{scl_prefix}git
%endif
BuildRequires: scl-utils-build, help2man

%description
This is the main package for %scl Software Collection, which install
the necessary packages to use subversion-1.9.0. Software collections 
allow to install more versions of the same package by using an 
alternative directory structure.
Install this package if you want to use subversion-1.9.0 on your system.

%package runtime
Summary: Package that handles %scl Software Collection.
Group: Applications/File
Requires: scl-utils
# e.g. scl-utils 20120927-8.el6_5
Requires: /usr/bin/scl_source
Requires(post): policycoreutils-python, libselinux-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: %{name}-runtime = %{version}
Requires: scl-utils-build
Group: Applications/File

%description build
Package shipping essential configuration macros to build
%scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl.
Group: Applications/File

%description scldevel
Development files for %scl (useful e.g. for hierarchical collection
building with transitive dependencies).

%prep
%setup -c -T

cat > README <<\EOF
%{expand:%(cat %{SOURCE0})}
EOF
# copy the license file so %%files section sees it
cp %{SOURCE1} .

%build
# temporary helper script used by help2man
cat > h2m_helper <<\EOF
#!/bin/sh
if [ "$1" = "--version" ]; then
  printf '%%s' "%{scl_name} %{version} Software Collection"
else
  cat README
fi
EOF
chmod a+x h2m_helper
# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# install generated man page
install -d -m 755               %{buildroot}%{_mandir}/man7
install -p -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/

%scl_install

# scldevel garbage
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

%post runtime
# Simple copy of context from system root to DSC root.
# In case new version needs some additional rules or context definition,
# it needs to be solved.
#semanage fcontext -a -e /usr/libexec/git-core/git-daemon /usr/libexec/git-core/%{scl_prefix}git-daemon >/dev/null 2>&1 || :
#semanage fcontext -a -e / %{_scl_root} >/dev/null 2>&1 || :
# T.B.D.
selinuxenabled && load_policy >/dev/null 2>&1 || :
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%files

%files runtime
%doc README LICENSE
%{_mandir}/man7/%{scl_name}.*
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Sat Mar 05 2016 Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.0
- initial spec for subversion19


