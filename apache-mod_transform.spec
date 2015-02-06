#Module-Specific definitions
%define mod_name mod_transform
%define mod_conf A46_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	XSLT and XIncludes Output filter for Apache 2
Name:		apache-%{mod_name}
Version:	0.6.0
Release:	38
Group:		System/Servers
License:	GPL
URL:		http://www.outoforder.cc/projects/apache/mod_transform/
Source0:	http://www.outoforder.cc/downloads/mod_transform/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= 2.0.54
Requires(pre):  apache >= 2.0.54
Requires:       apache-conf >= 2.0.54
Requires:       apache >= 2.0.54
BuildRequires:  apache-devel >= 2.0.54
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.11
BuildRequires:	libxslt-devel >= 1.1.5
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_transform is a filter module that allows Apache 2.0 to do
dynamic XSL Transformations on either static XML documents, or XML
documents generated from another Apache module or CGI program.

%prep

%setup -q -n %{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# fix apr
if [ -x %{_bindir}/apr-config ]; then APR=%{_bindir}/apr-config; fi || echo APR=%{_bindir}/apr-1-config
if [ -x %{_bindir}/apu-config ]; then APU=%{_bindir}/apu-config; fi || echo APU=%{_bindir}/apu-1-config
perl -pi -e "s|%{_bindir}/apr-config|$APR|g" m4/*.m4
perl -pi -e "s|%{_bindir}/apu-config|$APU|g" m4/*.m4

%build
libtoolize --copy --force; aclocal -I m4; automake --add-missing --copy --foreign; autoconf

%configure2_5x --localstatedir=/var/lib

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 src/.libs/libmod_transform.so %{buildroot}%{_libdir}/apache-extramodules/mod_transform.so
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}/var/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-37mdv2012.0
+ Revision: 772775
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-14
+ Revision: 678429
- mass rebuild

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-13mdv2011.0
+ Revision: 627737
- don't force the usage of automake1.7

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-12mdv2011.0
+ Revision: 588075
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-11mdv2010.1
+ Revision: 516196
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-10mdv2010.0
+ Revision: 406663
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-9mdv2009.1
+ Revision: 326268
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-8mdv2009.0
+ Revision: 235114
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-7mdv2009.0
+ Revision: 215655
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Thu Dec 20 2007 Olivier Blin <blino@mandriva.org> 0.6.0-6mdv2008.1
+ Revision: 135823
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-6mdv2008.0
+ Revision: 94137
- rebuilt due to missing packages

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-5mdv2008.0
+ Revision: 82687
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-4mdv2007.1
+ Revision: 140765
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-3mdv2007.1
+ Revision: 79529
- Import apache-mod_transform

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-3mdv2007.0
- rebuild

* Thu Apr 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-2mdk
- make it backportable

* Mon Dec 26 2005 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-1mdk
- initial Mandriva package

