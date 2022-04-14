# PE1 Routing Table & MPLS/LDP table

```
vagrant@pe1:~$ sh ip bgp
BGP table version is 5, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65000
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.11/32     0.0.0.0                  0         32768 i
  i10.0.0.12/32     10.0.0.12                0    100      0 i
*> 10.0.0.21/32     10.1.0.9                 0             0 65101 i
*>i10.0.0.22/32     10.0.0.12                0    100      0 65102 i
*> 100.64.1.0/24    10.1.0.9                 0             0 65101 i
*>i100.64.2.0/24    10.0.0.12                0    100      0 65102 i

Displayed  6 routes and 6 total paths


vagrant@pe1:~$ sh ip route
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

O>* 10.0.0.1/32 [110/2] via 10.1.0.1, eth1, label implicit-null, weight 1, 00:07:55
O   10.0.0.11/32 [110/1] via 0.0.0.0, dum0 onlink, weight 1, 00:08:16
C>* 10.0.0.11/32 is directly connected, dum0, 00:08:23
O>* 10.0.0.12/32 [110/3] via 10.1.0.1, eth1, label 17, weight 1, 00:07:55
B>* 10.0.0.21/32 [20/0] via 10.1.0.9, eth2, weight 1, 00:08:05
B>  10.0.0.22/32 [200/0] via 10.0.0.12 (recursive), weight 1, 00:07:51
  *                        via 10.1.0.1, eth1, label 17, weight 1, 00:07:51
O   10.1.0.0/30 [110/1] is directly connected, eth1, weight 1, 00:08:16
C>* 10.1.0.0/30 is directly connected, eth1, 00:08:23
O>* 10.1.0.4/30 [110/2] via 10.1.0.1, eth1, weight 1, 00:07:55
C>* 10.1.0.8/30 is directly connected, eth2, 00:08:23
B>* 100.64.1.0/24 [20/0] via 10.1.0.9, eth2, weight 1, 00:08:05
B>  100.64.2.0/24 [200/0] via 10.0.0.12 (recursive), weight 1, 00:07:51
  *                         via 10.1.0.1, eth1, label 17, weight 1, 00:07:51


vagrant@pe1:~$ sh mpls table
 Inbound Label  Type  Nexthop   Outbound Label
 -----------------------------------------------
 16             LDP   10.1.0.1  implicit-null
 17             LDP   10.1.0.1  17
```

# PING from isp1
```
vagrant@isp1:~$ ping 100.64.2.22 source-address 100.64.1.21 count 4
PING 100.64.2.22 (100.64.2.22) from 100.64.1.21 : 56(84) bytes of data.
64 bytes from 100.64.2.22: icmp_seq=1 ttl=61 time=2.36 ms
64 bytes from 100.64.2.22: icmp_seq=2 ttl=61 time=2.20 ms
64 bytes from 100.64.2.22: icmp_seq=3 ttl=61 time=1.89 ms
64 bytes from 100.64.2.22: icmp_seq=4 ttl=61 time=1.97 ms

--- 100.64.2.22 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 1.887/2.105/2.364/0.187 ms
```

# Capture on PE1-eth1
```
vagrant@pe1:~$ sudo tcpdump -n -i eth1
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
10:06:45.650096 MPLS (label 17, exp 0, [S], ttl 63) IP 100.64.1.21 > 100.64.2.22: ICMP echo request, id 24382, seq 1, length 64
10:06:45.651781 IP 100.64.2.22 > 100.64.1.21: ICMP echo reply, id 24382, seq 1, length 64
10:06:46.651748 MPLS (label 17, exp 0, [S], ttl 63) IP 100.64.1.21 > 100.64.2.22: ICMP echo request, id 24382, seq 2, length 64
10:06:46.653217 IP 100.64.2.22 > 100.64.1.21: ICMP echo reply, id 24382, seq 2, length 64
10:06:47.653202 MPLS (label 17, exp 0, [S], ttl 63) IP 100.64.1.21 > 100.64.2.22: ICMP echo request, id 24382, seq 3, length 64
10:06:47.654506 IP 100.64.2.22 > 100.64.1.21: ICMP echo reply, id 24382, seq 3, length 64
10:06:48.654525 MPLS (label 17, exp 0, [S], ttl 63) IP 100.64.1.21 > 100.64.2.22: ICMP echo request, id 24382, seq 4, length 64
10:06:48.655918 IP 100.64.2.22 > 100.64.1.21: ICMP echo reply, id 24382, seq 4, length 64
```
(replies are not inside MPLS because of PhP).

