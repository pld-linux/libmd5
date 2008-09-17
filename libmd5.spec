Summary:	RFC1321-based (RSA-free) MD5 library
Name:		libmd5
Version:	20020413
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libmd5-rfc/md5.tar.gz
# Source0-md5:	60f1691ece16bedc12dd2aa949cba606
URL:		http://sourceforge.net/projects/libmd5-rfc/
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86} %{x8664} alpha
%define		specflags	-DARCH_IS_BIG_ENDIAN=0
%endif
%ifarch sparc sparc64 powerpc ppc ppc64
%define		specflags	-DARCH_IS_BIG_ENDIAN=1
%endif
%ifarch arm
# detect endianess in runtime.
%endif

%description
This is a very small C library implementing RFC1321, the MD5 message
digest function. Unlike the existing W3C libmd5, it was written from
the specifications (not the sample code) in RFC1321, and therefore is
not required to acknowledge RSA in any way.

%package devel
Summary:	Header files for libmd5 library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libmd5 library.

%package static
Summary:	Static libmd5 library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmd5 library.

%prep
%setup -qc

%build
# with -prefer-pic you can link libmd5 statically in shared object.
libtool --mode=compile --tag=CC %{__cc} %{rpmcflags} -prefer-pic -shared -c md5.c
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -o libmd5.la md5.lo

# build and run testcase.
libtool --mode=compile --tag=CC %{__cc} %{rpmcflags} -static -c md5main.c
libtool --mode=link --tag=CC %{__cc} -o test md5main.lo libmd5.la -lm
./test --test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

install -D md5.h $RPM_BUILD_ROOT%{_includedir}/md5.h
libtool --mode=install cp libmd5.la $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmd5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmd5.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmd5.la
%{_libdir}/libmd5.so
%{_includedir}/md5.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libmd5.a
