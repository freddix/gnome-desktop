Summary:	GNOME desktop
Name:		gnome-desktop
Version:	3.10.0
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-desktop/3.10/%{name}-%{version}.tar.xz
# Source0-md5:	d9fd5ab4f8432c0a8876ed950565e0fb
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-doc-utils
BuildRequires:	gsettings-desktop-schemas-devel >= 3.10.0
BuildRequires:	gtk+3-devel >= 3.10.0
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	xorg-libxkbfile-devel
BuildRequires:	xkeyboard-config
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gsettings-desktop-schemas >= 3.10.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GNOME desktop library.

%package libs
Summary:	gnome-desktop library
Group:		Development/Libraries

%description libs
This package contains gnome-desktop library.

%package devel
Summary:	GNOME desktop includes
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
GNOME desktop header files.

%package apidocs
Summary:	gnome-desktop API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
gnome-desktop API documentation.

%prep
%setup -q

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__gtkdocize}
%{__intltoolize}
%{__gnome_doc_prepare}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules			\
	--disable-static			\
	--with-gnome-distributor="Freddix"	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,ig,kg,nds,ug,yo}

%find_lang %{name} --with-gnome --all-name

%clean
rm -fr $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/gnome-rr-debug
%{_datadir}/gnome/gnome-version.xml
%dir %{_datadir}/libgnome-desktop-3.0
%{_datadir}/libgnome-desktop-3.0/pnp.ids

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgnome-desktop-3.so.?
%attr(755,root,root) %{_libdir}/libgnome-desktop-3.so.*.*.*
%{_libdir}/girepository-1.0/GnomeDesktop-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-desktop-3.so
%{_datadir}/gir-1.0/GnomeDesktop-3.0.gir
%{_includedir}/gnome-desktop-3.0
%{_pkgconfigdir}/gnome-desktop-3.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}3

