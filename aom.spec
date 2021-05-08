%global sover           0
# git describe
%global aom_version     1.0.0-2227-gcfd59e96a

# Use commit with updated changelog for correct versioning
%global commit          9666276accea505cd14cbcb9e3f7ff5033da9172
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20190810
%global prerelease      1

Name:       aom
Version:    1.0.0
Release:    1
Summary:    Royalty-free next-generation video format

License:    BSD
URL:        http://aomedia.org/
Source0:    https://aomedia.googlesource.com/%{name}/+archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc-c++ gcc cmake3
BuildRequires:  doxygen git-core graphviz
BuildRequires:  perl-interpreter perl(Getopt::Long) perl-interpreter python3-devel yasm

Provides:       av1 = %{version}-%{release}
Requires:       libaom%{?_isa} = %{version}-%{release}

%description
The Alliance for Open Media’s focus is to deliver a next-generation
video format that is:

 - Interoperable and open;
 - Optimized for the Internet;
 - Scalable to any modern device at any bandwidth;
 - Designed with a low computational footprint and optimized for hardware;
 - Capable of consistent, highest-quality, real-time video delivery; and
 - Flexible for both commercial and non-commercial content, including
   user-generated content.

This package contains the reference encoder and decoder.

%package -n libaom
Summary:        Library files for aom

%description -n libaom
Library files for aom, the royalty-free next-generation
video format.

%package -n libaom-devel
Summary:        Development files for aom
Requires:       libaom%{?_isa} = %{version}-%{release}

%description -n libaom-devel
Development files for aom, the royalty-free next-generation
video format.

%prep
%autosetup -p1 -c %{name}-%{commit}
# Set GIT revision in version
sed -i 's@set(aom_version "")@set(aom_version "%{aom_version}")@' build/cmake/version.cmake

%build
mkdir _build && cd _build
%cmake3 ../ -DENABLE_CCACHE=1 \
            -DCMAKE_SKIP_RPATH=1 \
            -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%ifarch %{arm}
            -DAOM_NEON_INTRIN_FLAG=-mfpu=neon \
%endif
            -DCONFIG_WEBM_IO=1 \
            -DENABLE_DOCS=1 \
            -DCONFIG_ANALYZER=0 \
            -DCONFIG_LOWBITDEPTH=1
%make_build

%install
cd _build
%make_install

%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE PATENTS
%{_bindir}/aomdec
%{_bindir}/aomenc

%files -n libaom
%license LICENSE PATENTS
%{_libdir}/libaom.so.%{sover}

%files -n libaom-devel
%doc _build/docs/html/
%{_includedir}/%{name}
%{_libdir}/libaom.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri May 07 2021 weidong <weidong@uniontech.com> - 1.0.0-1
- Initial package.
