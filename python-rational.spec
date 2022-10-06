%define oname   rational
%define name    python-%oname
%define version 0.1
%define release 11


Summary:       Rational numbers for python
Name:          %{name}
Version:       0.0.4
Release:       1%{release}
Source0:       %{oname}.py
License:       LGPL
Group:         Development/Python
Url:           http://www.python.org/peps/pep-0239.html
BuildRequires: python

%description
This is a python module for rational numbers, following PEP 239,
with some extensions. While it is not as efficent as cRat, it is
more has some extra features (e.g., NaN and infinity handling).

%install
install -m644 -D %SOURCE0 $RPM_BUILD_ROOT/%{_libdir}/python%{py_ver}/site-packages/%{oname}.py
cd $RPM_BUILD_ROOT/%{_libdir}/python%{py_ver}/site-packages/
python -c "import %{oname}"

%files
%defattr(-,root,root)
%{_libdir}/python*/site-packages/%{oname}.py*


%changelog
* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 0.1-9mdv2010.0
+ Revision: 442480
- rebuild

* Sun Jan 04 2009 Funda Wang <fwang@mandriva.org> 0.1-8mdv2009.1
+ Revision: 324100
- rebuild

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 0.1-7mdv2009.0
+ Revision: 269041
- rebuild early 2009.0 package (before pixel changes)

* Sun May 11 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.1-6mdv2009.0
+ Revision: 205678
- Should not be noarch ed

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 0.1-5mdv2008.0
+ Revision: 69373
- use %%mkrel


* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 0.1-4mdk
- Really rebuild for new python

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 0.1-3mdk
- Rebuild for new python

* Sat Aug 09 2003 Austin Acton <aacton@yorku.ca> 0.1-2mdk
- python 2.3

* Wed Jul 09 2003 Austin Acton <aacton@yorku.ca> 0.1-1mdk 
- from andi payn <payn@myrealbox.com> :
  - initial specfile

