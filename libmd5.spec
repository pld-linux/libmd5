Summary:	RFC1321-based (RSA-free) MD5 library
Summary(pl.UTF-8):	Biblioteka MD5 oparta na RFC1321 (wolna od zobowiązań RSA)
Name:		libmd5
Version:	20020413
Release:	3
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libmd5-rfc/md5.tar.gz
# Source0-md5:	60f1691ece16bedc12dd2aa949cba606
Patch0:		%{name}-endian.patch
URL:		http://sourceforge.net/projects/libmd5-rfc/
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a very small C library implementing RFC1321, the MD5 message
digest function. Unlike the existing W3C libmd5, it was written from
the specifications (not the sample code) in RFC1321, and therefore is
not required to acknowledge RSA in any way.

%description -l pl.UTF-8
To jest bardzo mała biblioteka C zawierająca implementację RFC1321 -
funkcję skrótu MD5. W przeciwieństwie do istniejącej wcześniej libmd5
z W3C ta wersja została napisana na podstawie specyfikacji (a nie kodu
przykładowego) z RFC1321, więc nie wymaga jakiegokolwiek powoływania
się na RSA.

%package devel
Summary:	Header file for libmd5 library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libmd5
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	w3c-libwww-devel < 5.4.0-9

%description devel
Header file for libmd5 library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki libmd5.

%package static
Summary:	Static libmd5 library
Summary(pl.UTF-8):	Statyczna biblioteka libmd5
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	w3c-libwww-static < 5.4.0-9

%description static
Static libmd5 library.

%description static -l pl.UTF-8
Statyczna biblioteka libmd5.

%prep
%setup -qc
%patch0 -p1

%build
# with -prefer-pic you can link libmd5 statically in shared object.
libtool --mode=compile --tag=CC %{__cc} %{rpmcflags} -prefer-pic -shared -c md5.c
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -version-info 1:0:0 -o libmd5.la md5.lo

# build and run testcase.
%{__cc} %{rpmcflags} -c md5main.c
libtool --mode=link --tag=CC %{__cc} -o test md5main.o libmd5.la -lm
./test --test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

install -D md5.h $RPM_BUILD_ROOT%{_includedir}/md5.h
libtool --mode=install install libmd5.la $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmd5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmd5.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmd5.so
%{_libdir}/libmd5.la
%{_includedir}/md5.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libmd5.a
