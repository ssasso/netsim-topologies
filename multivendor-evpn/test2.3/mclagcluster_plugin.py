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

def transform_vtep_list(original, vteps_replacement, myself = ''):
    vteps = []
    for vt in original:
        if vt in vteps_replacement:
            repl = vteps_replacement[vt]
            if repl != myself:
                vteps.append(vteps_replacement[vt])
        else:
            vteps.append(vt)
    return list(dict.fromkeys(vteps))

def post_transform(topology: Box) -> None:
    print('MCLAG PLUGIN POST_TRANSFORM')
    vteps_replacement = {}
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
            # Consider also VXLAN ANYCAST VTEP
            if 'vxlan' in topology:
                # vtep address
                vtep_a = addressing.get(topology.pools, ['anycast_vtep', 'loopback'])['ipv4']
                print('    VTEP: {}'.format(vtep_a))
                for n in gdata.get('members', []):
                    if 'vtep' in topology.nodes[n].vxlan:
                        vteps_replacement[topology.nodes[n].vxlan.vtep] = str(vtep_a.network)
                    ifindex_offset = ( devices.get_device_attribute(topology.nodes[n], 'loopback_offset', topology.defaults) or 1 )
                    topology.nodes[n]['anycast_vtep'] = {
                            'loopback': ifindex_offset,
                            'address': str(vtep_a),
                            'plain_addr': str(vtep_a.network),
                            }
    print('VTEP REPLCS')
    print(vteps_replacement)
    for n, ndata in topology.nodes.items():
        myself = ''
        if 'anycast_vtep' in ndata:
            myself = ndata.anycast_vtep.plain_addr
        if 'vxlan' in ndata and ndata.vxlan.get('flooding', '') == 'static':
            ndata.vxlan.vtep_list = transform_vtep_list(ndata.vxlan.get('vtep_list', []), vteps_replacement, myself)
            ##### TODO: VTEP FLOOD LIST IS PER VNI!!!
    return

