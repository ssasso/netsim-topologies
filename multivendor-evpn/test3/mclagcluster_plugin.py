import os

from netsim.utils import log
from netsim.augment import addressing, devices
from box import Box
import netaddr

def init(topology: Box) -> None:
    print('MCLAG PLUGIN INIT')
    # Define custom data for lag, and set attribute to preserve
    topology.defaults.attributes.interface.lag.mclag = 'bool'
    topology.defaults.attributes.link.isl = 'bool'
    topology.defaults.attributes.node.mclagcluster = None
    return

def post_transform(topology: Box) -> None:
    print('MCLAG PLUGIN POST_TRANSFORM')
    for g,gdata in topology.get('groups', {}).items():
        mclagdata = gdata.get('node_data', {}).get('mclagcluster', {})
        if 'transit_vlan' in mclagdata and len(gdata.get('members', [])) == 2:
            print(' * G: {} - VL:{}'.format(g, mclagdata['transit_vlan']))
            # Handle transit VLAN
            # Allocate pool
            tvl_pool = addressing.get(topology.pools, ['transit', 'p2p'])['ipv4']
            print('    POOL = {}'.format(str(tvl_pool)))
            addr_id = 1
            for n in gdata.get('members', []):
                addr = tvl_pool.network + addr_id
                plen = tvl_pool.prefixlen
                ip_address = "{}/{}".format(addr, plen)
                print('      N: {} IP: {}'.format(n, ip_address))
                addr_id = addr_id + 1
                topology.nodes[n]['mclagcluster']['transit_ip'] = ip_address
    return

