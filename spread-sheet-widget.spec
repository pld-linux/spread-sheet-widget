#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Library for Gtk+ which provides a widget for viewing and manipulating 2 dimensional tabular data
Summary(pl.UTF-8):	Biblioteka Gtk+ zapewniająca widget do przeglądania i manipulowania dwuwymiarowymi danymi tabelarycznymi
Name:		spread-sheet-widget
Version:	0.6
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://alpha.gnu.org/gnu/ssw/%{name}-%{version}.tar.gz
# Source0-md5:	1db047605eedb0b63f7a34422a7889c6
Patch0:		%{name}-am.patch
Patch1:		%{name}-info.patch
URL:		https://www.gnu.org/software/ssw/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.10.1
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gtk+3-devel >= 3.18.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	texinfo
Requires:	glib2 >= 1:2.44
Requires:	gtk+3 >= 3.18.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Spread Sheet Widget is a library for Gtk+ which provides a widget
for viewing and manipulating 2 dimensional tabular data in a manner
similar to many popular spread sheet programs.

The design follows the model-view-controller paradigm and is of
complexity O(1) in both time and space. This means that it is
efficient and fast even for very large data.

Features commonly found in graphical user interfaces such as cut and
paste, drag and drop and row/column labelling are also included.

%description -l pl.UTF-8
GNU Spread Sheet Widget to biblioteka Gtk+, która udostępnia widget do
przeglądania i manipulowania dwuwymiarowymi danymi tabelarycznymi w
sposób zbliżony do wielu popularnych programów do obsługi arkuszy
kalkulacyjnych.

Projekt jest zgodny z paradygmatem model-widok-kontroler i ma
złożoność O(1) w czasie i przestrzeni. Oznacza to, że jest wydajny
nawet dla bardzo dużych zestawów danych.

Funkcje często spotykane w graficznych interfejsach użytkownika, takie
jak wycinanie, wklejanie, przeciąganie i upuszczanie oraz
etykietowanie wiersz / kolumna są również uwzględniane.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44
Requires:	gtk+3-devel >= 3.18.0

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libspread-sheet-widget.la

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libspread-sheet-widget.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspread-sheet-widget.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspread-sheet-widget.so
%{_includedir}/ssw-axis-model.h
%{_includedir}/ssw-sheet-axis.h
%{_includedir}/ssw-sheet.h
%{_includedir}/ssw-virtual-model.h
%{_pkgconfigdir}/spread-sheet-widget.pc
%{_infodir}/spread-sheet-widget.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libspread-sheet-widget.a
%endif
