Summary: A spelling checker
Name: aspell
Version: 0.60.6.1
Release: 3
License: LGPLv2 and MIT
Group: Applications/Text
URL: http://aspell.net/
Source0: ftp://ftp.gnu.org/gnu/aspell/aspell-%{version}.tar.gz
Patch1: aspell-0.50.3-gcc33.patch
Patch3: aspell-0.60.3-install_info.patch
Patch5: aspell-0.60.5-fileconflict.patch
Patch7: aspell-0.60.5-pspell_conf.patch
Patch8: aspell-0.60.6-zero.patch
Requires: aspell-en
BuildRequires: gettext, ncurses-devel, pkgconfig
Requires(pre): /sbin/install-info
Requires(preun): /sbin/install-info
Provides: pspell < 0.13
Obsoletes: pspell < 0.13
Conflicts: ispell < 3.1.21, aspell-pt_BR < 2.5, aspell-config < 0.27
Conflicts: aspell-de < 0.50, aspell-fr < 0.50, aspell-ca < 0.50, aspell-da < 0.50, aspell-es < 0.50, aspell-it < 0.50, aspell-nl < 0.50, aspell-no < 0.50, aspell-sv < 0.50

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%package devel
Summary: Static libraries and header files for Aspell development
Group: Development/Libraries
Requires: aspell = %{version}-%{release}
Requires: pkgconfig
Requires(pre): /sbin/install-info
Requires(preun): /sbin/install-info
Provides: pspell-devel < 0.13
Obsoletes: pspell-devel < 0.13

%description devel
Aspell is a spelling checker. The aspell-devel package includes the
static libraries and header files needed for Aspell development.

%prep
%setup -q -n aspell-%{version}/aspell
%patch1 -p1 -b .gcc33
%patch3 -p1 -b .iinfo
%patch5 -p1 -b .fc
%patch7 -p1 -b .mlib
%patch8 -p1 -b .zero
iconv -f windows-1252 -t utf-8 manual/aspell.info -o manual/aspell.info.aux
mv manual/aspell.info.aux manual/aspell.info

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/ispell ${RPM_BUILD_ROOT}%{_bindir}
mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/spell ${RPM_BUILD_ROOT}%{_bindir}

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libaspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libpspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/*-filter.la
chmod 644 ${RPM_BUILD_ROOT}%{_bindir}/aspell-import

%find_lang %{name}

%post   
/sbin/ldconfig
/sbin/install-info %{_infodir}/aspell.info.gz %{_infodir}/dir --entry="* Aspell: (aspell). "  || : 

%post devel
/sbin/install-info %{_infodir}/aspell-dev.info.gz %{_infodir}/dir --entry="* Aspell-dev: (aspell-dev). " || :

%preun 
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/aspell.info.gz %{_infodir}/dir 
fi
exit 0

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/aspell-dev.info.gz %{_infodir}/dir 
fi
exit 0

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO COPYING
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress
%{_libdir}/lib*.so.*
%{_libdir}/aspell-0.60/*
%{_datadir}/locale/*/LC_MESSAGES/aspell.mo
%{_infodir}/aspell.*
%{_mandir}/man1/aspell*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1.*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/lib*spell.so
%{_libdir}/pkgconfig/*
%{_infodir}/aspell-dev.*
%{_mandir}/man1/pspell-config.1*

