#
# Conditional build
%bcond_without	static_libs	# don't build static library
#
Summary:	Library for password quality checking and generating random passwords
Summary(pl.UTF-8):	Biblioteka do sprawdzania jakości oraz generowania losowych haseł
Name:		libpwquality
Version:	1.2.2
Release:	1
License:	BSD or GPL v2+
Group:		Libraries
Source0:	https://fedorahosted.org/releases/l/i/libpwquality/%{name}-%{version}.tar.bz2
# Source0-md5:	2105bb893791fe27efc20441e617f385
URL:		https://fedorahosted.org/libpwquality/
BuildRequires:	cracklib-devel >= 2.8
BuildRequires:	gettext-devel >= 0.15
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
Requires:	cracklib-dicts >= 2.8
Requires:	pam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libpwquality is a library for password quality checks and generation
of random passwords that pass the checks. This library uses the
cracklib and cracklib dictionaries to perform some of the checks.

%description -l pl.UTF-8
libpwquality to biblioteka do sprawdzania jakości haseł oraz
generowania haseł losowych przechodzących te testy. Biblioteka
wykorzystuje bibliotekę cracklib oraz słowniki crackliba do
wykonywania testów.

%package devel
Summary:	Header files for libpwquality library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libpwquality
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libpwquality library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libpwquality.

%package static
Summary:	Static libpwquality library
Summary(pl.UTF-8):	Statyczna biblioteka libpwquality
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libpwquality library.

%description static -l pl.UTF-8
Statyczna biblioteka libpwquality.

%package -n python-pwquality
Summary:	Python bindings for the libpwquality library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libpwquality
Group:		Libraries/Python
Requires:	%{name}-devel = %{version}-%{release}

%description -n python-pwquality
Python bindings for the libpwquality library.

%description -n python-pwquality -l pl.UTF-8
Wiązania Pythona do biblioteki libpwquality.

%prep
%setup -q

%build
%configure \
	--with-securedir=/%{_lib}/security \
	%{__enable_disable static_libs static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_pwquality.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/pwmake
%attr(755,root,root) %{_bindir}/pwscore
%attr(755,root,root) %{_libdir}/libpwquality.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpwquality.so.1
%attr(755,root,root) /%{_lib}/security/pam_pwquality.so
%config(noreplace) %verify(not md5 mtime size) /etc/security/pwquality.conf
%{_mandir}/man1/pwmake.1*
%{_mandir}/man1/pwscore.1*
%{_mandir}/man5/pwquality.conf.5*
%{_mandir}/man8/pam_pwquality.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpwquality.so
%{_libdir}/libpwquality.la
%{_includedir}/pwquality.h
%{_pkgconfigdir}/pwquality.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpwquality.a
%endif

%files -n python-pwquality
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pwquality.so
