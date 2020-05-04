#
# Conditional build
%bcond_without	python3		# Python 3 module
%bcond_without	static_libs	# don't build static library

Summary:	Library for password quality checking and generating random passwords
Summary(pl.UTF-8):	Biblioteka do sprawdzania jakości oraz generowania losowych haseł
Name:		libpwquality
Version:	1.4.2
Release:	1
License:	BSD or GPL v2+
Group:		Libraries
# Source0Download: https://github.com/libpwquality/libpwquality/releases
Source0:	https://github.com/libpwquality/libpwquality/releases/download/libpwquality-%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	ae6e61fc33f5dac0de5e847eb7520d71
URL:		https://github.com/libpwquality/libpwquality
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.9
BuildRequires:	cracklib-devel >= 2.8
BuildRequires:	gettext-tools >= 0.18.2
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
Suggests:	cracklib-dicts >= 2.8
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

%package -n pam-pam_pwquality
Summary:	PAM module for password quality checking using libpwquality
Summary(pl.UTF-8):	Moduł PAM do sprawdzania jakości haseł przy użyciu libpwquality
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_pwquality
PAM module for password quality checking using libpwquality.

%description -n pam-pam_pwquality -l pl.UTF-8
Moduł PAM do sprawdzania jakości haseł przy użyciu libpwquality.

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
Summary:	Python 2 bindings for the libpwquality library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libpwquality
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-pwquality
Python 2 bindings for the libpwquality library.

%description -n python-pwquality -l pl.UTF-8
Wiązania Pythona 2 do biblioteki libpwquality.

%package -n python3-pwquality
Summary:	Python 3 bindings for the libpwquality library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libpwquality
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-pwquality
Python 3 bindings for the libpwquality library.

%description -n python3-pwquality -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libpwquality.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-securedir=/%{_lib}/security \
	%{__enable_disable static_libs static}

%{__make}

cd python
CFLAGS="%{rpmcflags} -fno-strict-aliasing"
%py_build
cd ..

%if %{with python3}
cd python
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd python
%py_install
cd ..

%if %{with python3}
cd python
%py3_install
cd ..
%endif

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_pwquality.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_pwquality.a
%endif

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
%config(noreplace) %verify(not md5 mtime size) /etc/security/pwquality.conf
%{_mandir}/man1/pwmake.1*
%{_mandir}/man1/pwscore.1*
%{_mandir}/man5/pwquality.conf.5*

%files -n pam-pam_pwquality
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_pwquality.so
%{_mandir}/man8/pam_pwquality.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpwquality.so
%{_libdir}/libpwquality.la
%{_includedir}/pwquality.h
%{_pkgconfigdir}/pwquality.pc
%{_mandir}/man3/pwquality.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpwquality.a
%endif

%files -n python-pwquality
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pwquality.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/pwquality-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pwquality
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/pwquality.cpython-*.so
%{py3_sitedir}/pwquality-%{version}-py*.egg-info
%endif
