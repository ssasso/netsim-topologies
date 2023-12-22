import os

from netsim.utils import log
from netsim.augment import addressing, devices
from box import Box
import netaddr

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

def init(topology: Box) -> None:
    # Define custom data
    topology.defaults.attributes.group.vxlan_anycast = 'bool'
    return

def topology_expand(topology: Box) -> None:
    print('VXLAN_ANYCAST PLUGIN TOPOLOGY_EXPAND')
    # Expand the topology with loopback interfaces for anycast VTEPs
    loop_links = []
    for g,gdata in topology.get('groups', {}).items():
        # Run only for groups with vxlan_anycast: true
        if not gdata.get('vxlan_anycast', False):
            continue
        for n in gdata.get('members', []):
            loop_links.append({
                    n: None,
                    'type': 'loopback',
                    'pool': 'anycast_vtep',
                    'vxlan': { 'vtep': True },
                })
    topology.links = loop_links + topology.get('links',[]) # prepend new loopback links to topology links
    return

def post_transform(topology: Box) -> None:
    print('VXLAN_ANYCAST PLUGIN POST_TRANSFORM')
    vteps_replacement = {}
    # Generate ANYCAST VTEP Address for the groups
    for g,gdata in topology.get('groups', {}).items():
        # Run only for groups with vxlan_anycast: true
        if not gdata.get('vxlan_anycast', False):
            continue
        if 'vxlan' in topology:
            # vtep address - Replace currently allocated VTEP with a new anycast VTEP generated for the group
            vtep_a = addressing.get(topology.pools, ['anycast_vtep', 'loopback'])['ipv4']
            print('GRP {} - NEW VTEP: {}'.format(g,vtep_a))
            for n in gdata.get('members', []):
                if 'vtep' in topology.nodes[n].vxlan:
                    vteps_replacement[topology.nodes[n].vxlan.vtep] = str(vtep_a.network)
                topology.nodes[n]['anycast_vtep'] = {
                            'address': str(vtep_a),
                            'plain_addr': str(vtep_a.network),
                        }

    # Node data replacements:
    for n, ndata in topology.nodes.items():
        myself = ''
        # Change loopback interface address and VXLAN.vtep attribute
        if 'vxlan' in ndata and 'vtep' in ndata.vxlan and 'anycast_vtep' in ndata:
            myself = ndata.anycast_vtep.plain_addr
            old_vtep = ndata.vxlan.vtep + "/32"
            for intf in ndata.interfaces:
                if intf.get('ipv4', '') == old_vtep:
                    intf.ipv4 = ndata.anycast_vtep.address
                    intf.name = 'ANYCAST_VTEP'
                    break
            ndata.vxlan.vtep = myself
        # Replace remote vtep list in case of static flooding
        if 'vxlan' in ndata and ndata.vxlan.get('flooding', '') == 'static':
            ndata.vxlan.vtep_list = transform_vtep_list(ndata.vxlan.get('vtep_list', []), vteps_replacement, myself)
            for vl, vdata in ndata.get('vlans', {}).items():
                if 'vtep_list' in vdata:
                    vdata.vtep_list = transform_vtep_list(vdata.vtep_list, vteps_replacement, myself)
    return

