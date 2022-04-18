# NHRP, VyOS and Linux

Example topology of an overlay network based on mGRE/NHRP with VyOS and Linux.

* HUB: VyOS instance
* 4 x Spokes:
  * 2 x VyOS
  * 2 x Linux

In one linux instance, all the traffic is the the main routing table. On the second one, the "overlay" traffic is on the "overlay" VRF.

The VyOS spoke is configured to act as BGP RR for the overlay traffic. Every spoke is announcing a loopback IP addresses on the overlay space.

Spoke-to-Spoke traffic is allowed. However, it should be easy to force all the traffic to pass through the hub forcing it as next-hop.

