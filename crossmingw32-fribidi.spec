%define		realname   fribidi
Summary:	GNU FriBidi - library implementing the Unicode BiDi algorithm - cross MinGW32 version
Summary(pl.UTF-8):	GNU FriBidi - biblioteka implementująca algorytm Unicode BiDi - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	1.0.11
Release:	1
License:	LGPL v2.1+
Group:		Development/Libraries
#Source0Download: https://github.com/fribidi/fribidi/releases
Source0:	https://github.com/fribidi/fribidi/releases/download/v%{version}/%{realname}-%{version}.tar.xz
# Source0-md5:	06bb29553bb0529fb38648185f2553b0
URL:		https://fribidi.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	crossmingw32-gcc
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
GNU FriBidi is a free Implementation of the Unicode BiDi algorithm.

This package contains the cross version for Win32.

%description -l pl.UTF-8
GNU FriBidi to wolnodostępna implementacja algorytmu Unicode BiDi.

Paket ten zawiera wersję skrośną dla Win32.

%package static
Summary:	Static FriBidi library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka FriBidi (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static FriBidi library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka FriBidi (wersja skrośna MinGW32).

%package dll
Summary:	DLL FriBidi library for Windows
Summary(pl.UTF-8):	Biblioteka DLL FriBidi dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
DLL FriBidi library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL FriBidi dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-silent-rules \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man3
# runtime
%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.exe

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/libfribidi.dll.a
%{_libdir}/libfribidi.la
%{_includedir}/fribidi
%{_pkgconfigdir}/fribidi.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfribidi.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libfribidi-0.dll
