#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	libshout - icecast source streaming library (IDCJ modified version)
Summary(pl.UTF-8):	Biblioteka źródeł strumieni icecast (wersja zmodyfikowana IDCJ)
Name:		libshout-idjc
%define	basever	2.4.6
%define	rver	2
Version:	%{basever}.%{rver}
Release:	2
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://sourceforge.net/projects/libshoutidjc.idjc.p/files/
Source0:	https://downloads.sourceforge.net/libshoutidjc.idjc.p/%{name}-%{basever}-r%{rver}.tar.gz
# Source0-md5:	43746a012357781fd495cdbd39c25d19
URL:		https://idjc.sourceforge.io/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
BuildRequires:	libogg-devel
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	speex-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libshout is a library for communicating with and sending data to an
icecast server. It handles the socket connection, the timing of the
data, and prevents most bad data from getting to the icecast server.

%description -l pl.UTF-8
libshout to biblioteka do komunikowania się z i wysyłania danych do
serwera icecast. Obsługuje połączenia, czasy danych i zapobiega
dotarciu większości złych danych do serwera icecast.

%package devel
Summary:	Icecast source streaming library development package (IDCJ modified version)
Summary(pl.UTF-8):	Pakiet dla programistów używających libshout (wersja zmodyfikowana IDCJ)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libogg-devel
Requires:	libtheora-devel
Requires:	libvorbis-devel
Requires:	openssl-devel
Requires:	speex-devel

%description devel
The libshout-devel package contains the header files needed for
developing applications that send data to an icecast server. Install
libshout-devel if you want to develop applications using libshout.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji
wysyłających dane do serwera icecast.

%package static
Summary:	Icecast source streaming static library (IDCJ modified version)
Summary(pl.UTF-8):	Statyczna biblioteka libshout (wersja zmodyfikowana IDCJ)
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Icecast source streaming static library.

%description static -l pl.UTF-8
Statyczna biblioteka libshout - źródeł strumieni icecast.

%prep
%setup -q -n %{name}-%{basever}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libshout-idjc.la
# ckport support is not maintained in PLD
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/ckport
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libshout-idjc

cp -p examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/shoutidjc
%attr(755,root,root) %{_libdir}/libshout-idjc.so.*.*.*
%ghost %{_libdir}/libshout-idjc.so.3
%{_mandir}/man1/shoutidjc.1*

%files devel
%defattr(644,root,root,755)
%doc doc/libshout.xml
%{_libdir}/libshout-idjc.so
%{_includedir}/shoutidjc
%{_pkgconfigdir}/shout-idjc.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libshout-idjc.a
%endif
