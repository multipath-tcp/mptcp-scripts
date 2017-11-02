%global             cbq_version v0.7.3
Summary:            Advanced IP routing and network device configuration tools
Name:               iproute
Version:            mptcp_v0.93
Release:            4%{?dist}
Group:              Applications/System
URL:                https://github.com/multipath-tcp/iproute-mptcp
Source0:            https://github.com/multipath-tcp/iproute-mptcp/archive/mptcp_v0.93.zip

License:            GPLv2+ and Public Domain
BuildRequires:      bison
BuildRequires:      elfutils-libelf-devel
BuildRequires:      flex
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libdb-devel
BuildRequires:      libmnl-devel
BuildRequires:      libselinux-devel
BuildRequires:      linuxdoc-tools
BuildRequires:      pkgconfig
BuildRequires:      psutils
BuildRequires:      tex(cm-super-t1.enc)
BuildRequires:      tex(dvips)
BuildRequires:      tex(ecrm1000.tfm)
BuildRequires:      tex(latex)
%if 0%{?fedora}
BuildRequires:      linux-atm-libs-devel
%endif
# For the UsrMove transition period
Conflicts:          filesystem < 3
Provides:           /sbin/ip

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
2.4.x and 2.6.x kernel.

%package doc
Summary:            Documentation for iproute2 utilities with examples
Group:              Applications/System
License:            GPLv2+

%description doc
The iproute documentation contains howtos and examples of settings.

%package devel
Summary:            iproute development files
Group:              Development/Libraries
License:            GPLv2+
Provides:           iproute-static = %{version}-%{release}

%description devel
The libnetlink static library.

%prep
%setup -q -n iproute-mptcp-%{version}

%build
export CFLAGS="%{optflags}"
export LIBDIR=/%{_libdir}
export IPT_LIB_DIR=/%{_lib}/xtables
./configure
make %{?_smp_mflags}
make -C doc

%install
export DESTDIR='%{buildroot}'
export SBINDIR='%{_sbindir}'
export MANDIR='%{_mandir}'
export LIBDIR='%{_libdir}'
export CONFDIR='%{_sysconfdir}/iproute2'
export DOCDIR='%{_docdir}'
make install

# libnetlink
install -D -m644 include/libnetlink.h %{buildroot}%{_includedir}/libnetlink.h
install -D -m644 lib/libnetlink.a %{buildroot}%{_libdir}/libnetlink.a

# drop these files, iproute-doc package extracts files directly from _builddir
rm -rf '%{buildroot}%{_docdir}'

%files
%dir %{_sysconfdir}/iproute2
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README README.decnet README.iproute2+tc README.distribution README.lnstat
%{_mandir}/man7/*
%{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%{_datadir}/bash-completion/completions/tc

%files doc
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc doc/*.ps
%doc examples

%files devel
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man3/*
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Phil Sutter <psutter@redhat.com> - 4.4.0-1
- New version 4.4.0

* Sun Oct 04 2015 Phil Sutter <psutter@redhat.com> - 4.2.0-4
- Simplify RPM install stage by using package's install target

* Sun Oct 04 2015 Phil Sutter <psutter@redhat.com> - 4.2.0-3
- Add missing build dependency to libmnl-devel
- Ship tipc utility

* Thu Sep 24 2015 Phil Sutter <psutter@redhat.com> - 4.2.0-2
- Add missing build dependency to libselinux-devel

* Wed Sep 02 2015 Pavel Šimerda <psimerda@redhat.com> - 4.2.0-1
- new version 4.2.0

* Tue Jul 07 2015 Pavel Šimerda <psimerda@redhat.com> - 4.1.1-1
- new version 4.1.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Pavel Šimerda <psimerda@redhat.com> - 4.0.0-3
- remove patch rejected by upstream

* Mon May 11 2015 Pavel Šimerda <psimerda@redhat.com> - 4.0.0-2
- Remove patch rejected by upstream

* Tue Apr 14 2015 Pavel Šimerda <psimerda@redhat.com> - 4.0.0-1
- new version 4.0.0

* Fri Mar 13 2015 Pavel Šimerda <psimerda@redhat.com> - 3.19.0-1
- new version 3.19.0

* Sat Oct 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.16.0-3
- Backport fix for ip link add name regression that broke libvirt

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Petr Šabata <contyk@redhat.com> - 3.16.0-1
- 3.16 bump

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 3.15.0-2
- fix license handling

* Thu Jun 12 2014 Petr Šabata <contyk@redhat.com> - 3.15.0-1
- 3.15.0 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Petr Šabata <contyk@redhat.com> - 3.14.0-2
- Fix incorrect references in ss(8), #1092653

* Tue Apr 15 2014 Petr Šabata <contyk@redhat.com> - 3.14.0-1
- 3.14 bump
- Drop out iplink_have_newlink() fix in favor of upstream's approach

* Tue Nov 26 2013 Petr Šabata <contyk@redhat.com> - 3.12.0-2
- Drop libnl from dependencies (#1034454)

* Mon Nov 25 2013 Petr Šabata <contyk@redhat.com> - 3.12.0-1
- 3.12.0 bump

* Thu Nov 21 2013 Petr Šabata <contyk@redhat.com> - 3.11.0-2
- Fix the rtt time parsing again

* Tue Oct 22 2013 Petr Šabata <contyk@redhat.com> - 3.11.0-1
- 3.11 bump

* Tue Oct 01 2013 Petr Pisar <ppisar@redhat.com> - 3.10.0-8
- Close file with bridge monitor file (bug #1011822)

* Tue Sep 24 2013 Petr Pisar <ppisar@redhat.com> - 3.10.0-7
- Add tc -OK option
- Document "bridge mdb" and "bridge monitor mdb"

* Fri Aug 30 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-6
- Fix lnstat -i properly this time

* Thu Aug 29 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-5
- Fix an 'ip link' hang (#996537)

* Tue Aug 13 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-4
- lnstat -i: Run indefinitely if the --count isn't specified (#977845)
- Switch to unversioned %%docdir

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-2
- Fix the XFRM patch

* Wed Jul 17 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-1
- 3.10.0 bump
- Drop the SHAREDIR patch and revert to upstream ways (#966445)
- Fix an XFRM regression with FORTIFY_SOURCE

* Tue Apr 30 2013 Petr Šabata <contyk@redhat.com> - 3.9.0-1
- 3.9.0 bump

* Thu Apr 25 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-4
- ATM is available in Fedora only

* Tue Mar 12 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-3
- Mention the "up" argument in documentation and help outputs (#907468)

* Mon Mar 04 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-2
- Bump for 1.4.18 rebuild

* Tue Feb 26 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-1
- 3.8.0 bump

* Fri Feb 08 2013 Petr Šabata <contyk@redhat.com> - 3.7.0-2
- Don't propogate mounts out of ip (#882047)

* Wed Dec 12 2012 Petr Šabata <contyk@redhat.com> - 3.7.0-1
- 3.7.0 bump

* Mon Nov 19 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-3
- Include section 7 manpages (#876857)
- Fix ancient bogus dates in the changelog (correction based upon commits)
- Explicitly require some TeX fonts no longer present in the base distribution

* Thu Oct 04 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-2
- List all interfaces by default

* Wed Oct 03 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-1
- 3.6.0 bump

* Thu Aug 30 2012 Petr Šabata <contyk@redhat.com> - 3.5.1-2
- Remove the explicit iptables dependency (#852840)

* Tue Aug 14 2012 Petr Šabata <contyk@redhat.com> - 3.5.1-1
- 3.5.1 bugfix release bump
- Rename 'br' to 'bridge'

* Mon Aug 06 2012 Petr Šabata <contyk@redhat.com> - 3.5.0-2
- Install the new bridge utility

* Thu Aug 02 2012 Petr Šabata <contyk@redhat.com> - 3.5.0-1
- 3.5.0 bump
- Move to db5.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Petr Šabata <contyk@redhat.com> - 3.4.0-1
- 3.4.0 bump
- Drop the print route patch (included upstream)

* Mon Apr 30 2012 Petr Šabata <contyk@redhat.com> - 3.3.0-2
- Let's install rtmon too... (#814819)

* Thu Mar 22 2012 Petr Šabata <contyk@redhat.com> - 3.3.0-1
- 3.3.0 bump
- Update source URL

* Mon Feb 27 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-3
- Address dangerous /tmp files security issue (CVE-2012-1088, #797881, #797878)

* Fri Jan 27 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-2
- Simplify the spec a bit thanks to the UsrMove feature

* Fri Jan 06 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-1
- 3.2.0 bump
- Removing a useless, now conflicting patch (initcwnd already decumented)

* Thu Nov 24 2011 Petr Šabata <contyk@redhat.com> - 3.1.0-1
- 3.1.0 bump
- Point URL and Source to the new location on kernel.org
- Remove now obsolete defattr
- Dropping various patches now included upstream
- Dropping iproute2-2.6.25-segfault.patch; I fail to understand the reason for
  this hack

* Tue Nov 15 2011 Petr Šabata <contyk@redhat.com> - 2.6.39-6
- ss -ul should display UDP CLOSED sockets (#691100)

* Thu Oct 06 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-5
- Fix ss, lnstat and arpd usage and manpages

* Wed Sep 07 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-4
- lnstat should dump (-d) to stdout instead of stderr (#736332)

* Tue Jul 26 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-3
- Rebuild for xtables7

* Tue Jul 12 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-2
- Rebuild for xtables6

* Thu Jun 30 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-1
- 2.6.39 bump

* Wed Apr 27 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-4
- Link [cr]tstat to lnstat

* Wed Apr 27 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-3
- Install ctstat, rtstat and routef manpage symlinks
- Install m_xt & m_ipt tc modules
- Creating devel and virtual static subpackages with libnetlink

* Thu Apr 21 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-2
- General cleanup
- Use global instead of define
- Buildroot removal
- Correcting URL and Source links
- Install genl, ifstat, routef, routel and rtpr (rhbz#697319)

* Fri Mar 18 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-1
- 2.6.38.1 bump

* Wed Mar 16 2011 Petr Sabata <psabata@redhat.com> - 2.6.38-1
- 2.6.38 bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Petr Sabata <psabata@redhat.com> - 2.6.37-2
- man-pages.patch update, ip(8) TYPE whitespace

* Mon Jan 10 2011 Petr Sabata <psabata@redhat.com> - 2.6.37-1
- 2.6.37 upstream release
- ss(8) improvements patch removed (included upstream)

* Wed Dec 08 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-10
- fix a typo in ss(8) improvements patch, rhbz#661267

* Tue Nov 30 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-9
- ss(8) improvements patch by jpopelka; should be included in 2.6.36

* Tue Nov 09 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-8
- rhbz#641599, use the versioned path, man-pages.patch update, prep update

* Tue Oct 12 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-7
- Do not segfault if peer name is omitted when creating a peer veth link, rhbz#642322

* Mon Oct 11 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-6
- Man-pages update, rhbz#641599

* Wed Sep 29 2010 jkeating - 2.6.35-5
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-4
- Modified man-pages.patch to fix cbq manpage, rhbz#635877

* Tue Sep 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-3
- Don't print routes with negative metric fix, rhbz#628739

* Wed Aug 18 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-2
- 'ip route get' fix, iproute2-2.6.35-print-route.patch
- rhbz#622782

* Thu Aug 05 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-1
- 2.6.35 version bump
- iproute2-tc-priority.patch removed (included in upstream now)

* Thu Jul 08 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-5
- Licensing guidelines compliance fix

* Wed Jul 07 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-4
- Requires: iptables >= 1.4.5, BuildRequires: iptables-devel >= 1.4.5

* Thu Jul 01 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-3
- Build now runs ./configure to regenerate Makefile for ipt/xt detection

* Mon Jun 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-2
- iproute-tc-priority.patch, rhbz#586112

* Mon Jun 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-1
- 2.6.34 version bump

* Tue Apr 20 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.33-2
- 578729 6rd tunnel correctly 3979ef91de9ed17d21672aaaefd6c228485135a2
- change BR texlive to tex according to guidelines

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.33-1
- update

* Tue Jan 26 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.32-2
- add macvlan aka VESA support d63a9b2b1e4e3eab0d0577d0a0f412d50be1e0a7
- kernel headers 2.6.33 ab322673298bd0b8927cdd9d11f3d36af5941b93
  are needed for macvlan features and probably for other added later.
- fix number of release which contains 2.6.32 kernel headers and features
  but it was released as 2.6.31

* Mon Jan  4 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.31-1
- update to 2.6.31

* Fri Nov 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.1.20091106gita7a9ddbb
- 539232 patch cbq initscript

* Fri Nov 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.0.20091106gita7a9ddbb
- snapshot with kernel headers for 2.6.32

* Fri Oct  9 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.0.20091009gitdaf49fd6
- new official version isn't available but it's needed -> switch to git snapshots

* Thu Sep 24 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5
- create missing man pages

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-3
- new iptables (xtables) bring problems to tc, when ipt is used. 
  rhbz#497344 still broken. tc_modules.patch brings correct paths to
  xtables, but that doesn't fix whole issue.
- 497355 ip should allow creation of an IPsec SA with 'proto any' 
  and specified sport and dport as selectors

* Tue Apr 14 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-2
- c3651bf4763d7247e3edd4e20526a85de459041b ip6tunnel: Fix no default 
 display of ip4ip6 tunnels
- e48f73d6a5e90d2f883e15ccedf4f53d26bb6e74 missing arpd directory

* Wed Mar 25 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-1
- update to 2.6.29
- remove DDR patch which became part of sourc
- add patch with correct headers 1957a322c9932e1a1d2ca1fd37ce4b335ceb7113

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-2
- 483484 install distribution files into /usr/share and also fixed
 install paths in spec
- add the latest change from git which add DRR support
 c86f34942a0ce9f8203c0c38f9fe9604f96be706

* Mon Jan 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-1
- previous two patches were included into 2.6.28 release.
- update

* Mon Jan 12 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.27-2
- 475130 - Negative preferred lifetimes of IPv6 prefixes/addresses
  displayed incorrectly
- 472878 - “ip maddr show” in IB interface causes a stack corruption
- both patches will be probably in iproute v2.6.28

* Thu Dec 4 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.27-1
- aead support was included into upstream version
- patch for moving libs is now deprecated
- update to 2.6.27

* Tue Aug 12 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.26-1
- update to 2.6.26
- clean patches

* Tue Jul 22 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-5
- fix iproute2-2.6.25-segfault.patch

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.6.25-4
- rebuild for new db4-4.7

* Thu Jul  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-3
- 449933 instead of failing strncpy use copying byte after byte

* Wed May 14 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-2
- allow replay setting, solve also 444724

* Mon Apr 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-1
- update
- remove patch for backward compatibility
- add patch for AEAD compatibility

* Thu Feb 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-4
- add creating ps file again. Fix was done in texlive

* Wed Feb  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-3
- rebuild without tetex files. It isn't working in rawhide yet. Added
  new source for ps files. 
- #431179 backward compatibility for previous iproute versions

* Mon Jan 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-2
- rebuild with fix tetex and linuxdoc-tools -> manual pdf
- clean unnecessary patches
- add into spec *.so objects, new BR linux-atm-libs-devel

* Wed Oct 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-1
- new version from upstrem 2.3.23

* Tue Oct 23 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-5
- move files from /usr/lib/tc to /usr/share/tc
- remove listing files twice

* Fri Aug 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-3
- package review #225903

* Mon Aug 27 2007 Jeremy Katz <katzj@redhat.com> - 2.6.22-2
- rebuild for new db4

* Wed Jul 11 2007 Radek Vokál <rvokal@redhat.com> - 2.6.22-1
- upgrade to 2.6.22

* Mon Mar 19 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-2
- fix broken tc-pfifo man page (#232891)

* Thu Mar 15 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-1
- upgrade to 2.6.20

* Fri Dec 15 2006 Radek Vokál <rvokal@redhat.com> - 2.6.19-1
- upgrade to 2.6.19

* Mon Dec 11 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-5
- fix snapshot version

* Fri Dec  1 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-4
- spec file cleanup
- one more rebuilt against db4

* Thu Nov 16 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-3
- fix defective manpage for tc-pfifo (#215399)

* Mon Nov 13 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-2
- rebuilt against new db4

* Tue Oct  3 2006 Radek Vokal <rvokal@redhat.com> - 2.6.18-1
- upgrade to upstream 2.6.18
- initcwnd patch merged
- bug fix for xfrm monitor
- alignment fixes for cris
- documentation corrections
        
* Mon Oct  2 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-7
- fix ip.8 man page, add initcwnd option

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-5
- fix crash when resolving ip address

* Mon Aug 21 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-4
- add LOWER_UP and DORMANT flags (#202199)
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-3.1
- rebuild

* Mon Jun 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-3
- improve handling of initcwnd value (#179719)

* Sun May 28 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-2
- fix BuildRequires: flex (#193403)

* Sun Mar 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-1
- upgrade to 2.6.16-060323
- don't hardcode /usr/lib in tc (#186607)

* Wed Feb 22 2006 Radek Vokál <rvokal@redhat.com> - 2.6.15-2
- own /usr/lib/tc (#181953)
- obsoletes shapecfg (#182284)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Radek Vokal <rvokal@redhat.com> 2.6.15-1
- upgrade to 2.6.15-060110

* Mon Dec 12 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-11
- rebuilt

* Fri Dec 09 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-10
- remove backup of config files (#175302)

* Fri Nov 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-9
- use tc manpages and cbq.init from source tarball (#172851)

* Thu Nov 10 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-8
- new upstream source 

* Mon Oct 31 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-7
- add warning to ip tunnel add command (#128107)

* Fri Oct 07 2005 Bill Nottingham <notting@redhat.com> 2.6.14-6
- update from upstream (appears to fix #170111)

* Fri Oct 07 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-5
- update from upstream
- fixed host_len size for memcpy (#168903) <Matt_Domsch@dell.com>

* Fri Sep 23 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-4
- add RPM_OPT_FLAGS

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-3
- forget to apply the patch :( 

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-2
- make ip help work again (#168449)

* Wed Sep 14 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-1
- upgrade to ss050901 for 2.6.14 kernel headers

* Fri Aug 26 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-3
- added /sbin/cbq script and sample configuration files (#166301)

* Fri Aug 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-2
- upgrade to iproute2-050816

* Thu Aug 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-1
- update to snapshot for 2.6.13+ kernel

* Tue May 24 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-2
- removed useless initvar patch (#150798)
- new upstream source 

* Tue Mar 15 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-1
- update to iproute-2.6.11

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-2
- gcc4 rebuilt

* Wed Feb 16 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-1
- update to iproute-2.6.10

* Thu Dec 23 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-6
- added arpd into sbin

* Mon Nov 29 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-5
- debug info removed from makefile and from spec (#140891)

* Tue Nov 16 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-4
- source file updated from snapshot version
- endian patch adding <endian.h> 

* Sat Sep 18 2004 Joshua Blanton <jblanton@cs.ohiou.edu> 2.6.9-3
- added installation of netem module for tc

* Mon Sep 06 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-2
- fixed possible buffer owerflow, path by Steve Grubb <linux_4ever@yahoo.com>

* Wed Sep 01 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-1
- updated to iproute-2.6.9, spec file change, patches cleared

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 26 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-16
- Took tons of manpages from debian, much more complete (#123952).

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-15
- rebuilt

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-13.2
- Built security errata version for FC1.

* Wed Apr 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-14
- Fixed -f option for ss (#118355).
- Small description fix (#110997).
- Added initialization of some vars (#74961). 
- Added patch to initialize "default" rule as well (#60693).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Nov 05 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-12
- Security errata for netlink (CAN-2003-0856).

* Thu Oct 23 2003 Phil Knirsch <pknirsch@redhat.com>
- Updated to latest version. Used by other distros, so seems stable. ;-)
- Quite a few patches needed updating in that turn.
- Added ss (#107363) and several other new nifty tools.

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-7
- Added htb3-tc patch from http://luxik.cdi.cz/~devik/qos/htb/ (#75486).

* Fri Oct 11 2002 Bill Nottingham <notting@redhat.com> 2.4.7-6
- remove flags patch at author's request

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-4
- Don't forcibly strip binaries

* Mon May 27 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-3
- Fixed missing diffserv and atm support in config (#57278).
- Fixed inconsistent numeric base problem for command line (#65473).

* Tue May 14 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-2
- Added patch to fix crosscompiling by Adrian Linkins.

* Fri Mar 15 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-1
- Update to latest stable release 2.4.7-now-ss010824.
- Added simple man page for ip.

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- allow setting of allmulti & promisc flags (#48669)

* Mon Jul 02 2001 Than Ngo <than@redhat.com>
- fix build problem in beehive if kernel-sources is not installed

* Fri May 25 2001 Helge Deller <hdeller@redhat.de>
- updated to iproute2-2.2.4-now-ss001007.tar.gz 
- bzip2 source tar file
- "License" replaces "Copyright"
- added "BuildPrereq: tetex-latex tetex-dvips psutils"
- rebuilt for 7.2

* Tue May  1 2001 Bill Nottingham <notting@redhat.com>
- use the system headers - the included ones are broken
- ETH_P_ECHO went away

* Sat Jan  6 2001 Jeff Johnson <jbj@redhat.com>
- test for specific KERNEL_INCLUDE directories.

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- rebuild for 7.1

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- add default configuration files for iproute (Bug #10549, #18887)

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- fix include-glibc/ to cope with glibc 2.2 new resolver headers

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment
- use RPM macros
- handle RPM_OPT_FLAGS

* Sat Jun 03 2000 Than Ngo <than@redhat.de>
- fix iproute to build with new glibc

* Fri May 26 2000 Ngo Than <than@redhat.de>
- update to 2.2.4-now-ss000305
- add configuration files

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Mon Aug 16 1999 Cristian Gafton <gafton@redhat.com>
- first build
