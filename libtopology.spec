name:		libtopology
Version:	0.3
Release:	7%{?dist}
Summary:	CPU Topology library

Group:		System Environment/Libraries
License:	LGPLv2
URL:		http://libtopology.ozlabs.org/

Source0:	http://libtopology.ozlabs.org/releases/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-build-%(%{__id_u} -n)

%description
Libtopology is a library for discovering the hardware topology on Linux
systems.

%package devel
Summary:	CPU Topology library development package
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development package for libtopology.

%package doc
Summary:	CPU Topology library documentation package
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
BuildRequires:	doxygen
BuildArch:	noarch

%description doc
Documentation and sample programs for libtopology.

%prep
%setup -q -n %{name}-%{version}

%build
make	CFLAGS="%{optflags} -fPIC" %{?_smp_mflags}
make	doc

%check
make	CFLAGS="%{optflags} -fPIC" test

%install
rm -rf %{buildroot}
make	inst_libdir="%{buildroot}/%{_prefix}/%{_lib}" \
	inst_includedir="%{buildroot}/%{_includedir}" \
	install

mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/{examples,doc}
cp -p COPYING README %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/
cp -p programs/*.c %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/examples/.
cp -p include/compat.h %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/examples/.
# We shouldn't package fonts.  They're not required.
[ -e doc/generated/latex/FreeSans.ttf ] && rm doc/generated/latex/FreeSans.ttf 
cp -pr doc/generated/* %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/doc/.

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libtopology.so.0
%{_libdir}/libtopology.so.0.3
%dir %{_defaultdocdir}/%{name}-%{version}/
%{_defaultdocdir}/%{name}-%{version}/COPYING

%files devel 
%defattr(-,root,root,-)
%{_includedir}/topology.h
%{_libdir}/libtopology.so

%files doc 
%defattr(-,root,root,-)
%{_defaultdocdir}/%{name}-%{version}/README
%{_defaultdocdir}/%{name}-%{version}/examples/
%{_defaultdocdir}/%{name}-%{version}/doc

%changelog
* Tue Aug 11 2009 tony@bakeyournoodle.com - 0.3-7
- Fix FTBS problem (#511641)
- Also split documentation into (noarch) subpackage

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Tony Breeds <tony@bakeyournoodle.com> 0.3-4
- Conform with the new font packageing guidelines (#477415)

* Tue Nov 12 2008 Tony Breeds <tony@bakeyournoodle.com> 0.3-0.3
- Add BuildRequires for doxygen to the -devel package.

* Mon Nov 10 2008 Tony Breeds <tony@bakeyournoodle.com> 0.3-0.2
- move docs from seperate package into -devel
- use correct licence
- use cp -p for install

* Wed Oct 22 2008 Tony Breeds <tony@bakeyournoodle.com> 0.3-0.1
- Initial RPM package for Fedora
