Summary:	RFC1321-based (RSA-free) MD5 library
Name:		libmd5
Version:	20020413
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libmd5-rfc/md5.tar.gz
# Source0-md5:	60f1691ece16bedc12dd2aa949cba606
URL:		http://sourceforge.net/projects/libmd5-rfc/
BuildRequires:	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -qcn %{name}-%{version}

%build
%{__cc} %{rpmcflags} -O3 -funroll-loops -fpic -c md5.c
%{__ar} rc libmd5.a md5.o
%{__cc} md5.o -shared -o libmd5.so -Wl,-soname=libmd5.so.0 && /sbin/ldconfig -n .

# build and run testcase.
%{__cc} md5main.c -o test ./libmd5.so -lm
LD_PRELOAD=./libmd5.so ./test --test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

install -D md5.h $RPM_BUILD_ROOT%{_includedir}/md5.h
install libmd5.* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmd5.so
%{_includedir}/md5.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libmd5.a
