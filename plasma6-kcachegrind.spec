%define git 20240217
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")
Summary:	Visualisation tool for profiling data generated by Cachegrind and Calltree
Name:		plasma6-kcachegrind
Version:	24.01.96
Release:	%{?git:0.%{git}.}1
Group:		Graphical desktop/KDE
License:	GPLv2+
Url:		https://www.kde.org
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%if 0%{?git:1}
Source0:	https://invent.kde.org/sdk/kcachegrind/-/archive/%{gitbranch}/kcachegrind-%{gitbranchd}.tar.bz2#/kcachegrind-%{git}.tar.bz2
%else
Source0:	https://download.kde.org/%{stable}/release-service/%{version}/src/kcachegrind-%{version}.tar.xz
%endif
#Patch0:		kcachegrind-ecm.patch
BuildRequires: 	cmake
BuildRequires: 	cmake(ECM)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6QmlCore)
BuildRequires:  cmake(Qt6QmlNetwork)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(KF6Archive)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6DBusAddons)
BuildRequires:	cmake(KF6DocTools)
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(KF6XmlGui)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6KIO)
BuildRequires:  qt6-qtbase-theme-gtk3
Requires:	valgrind

%description
KCachegrind is a visualisation tool for the profiling data generated by
Cachegrind and Calltree (they profile data file format is upwards compatible).
Calltree extends Cachegrind, which is part of Valgrind.

%files -f kcachegrind.lang
%{_bindir}/kcachegrind
%{_bindir}/dprof2calltree
%{_bindir}/hotshot2calltree
%{_bindir}/memprof2calltree
%{_bindir}/op2calltree
%{_bindir}/pprof2calltree
%{_datadir}/kcachegrind
%{_datadir}/applications/org.kde.kcachegrind.desktop
%{_datadir}/metainfo/org.kde.kcachegrind.appdata.xml
%{_iconsdir}/*/*/*/kcachegrind*

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n kcachegrind-%{?git:%{gitbranchd}}%{!?git:%{version}}
# FIXME https://github.com/llvm/llvm-project/issues/80435
export CC=gcc
export CXX=g++
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja -C build

%install
%ninja_install -C build
%find_lang kcachegrind --with-html --with-qt
