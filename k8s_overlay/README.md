# K8S and Custom Overlay networks

Creating a K3S cluster on a pool of 3 linux VMs.

Using a dedicated custom overlay network which uses EVPN+VXLAN L2 topology, extending it to the K8S Pods with Multus+Bridge.

The "birds" testing Pods will create a BGP session OVER the overlay with the hub, and announce a loopback IP.

