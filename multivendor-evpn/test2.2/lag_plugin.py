import os

from netsim.utils import log
from box import Box

def init(topology: Box) -> None:
    print('LAG PLUGIN INIT')
    # Define custom data for lag, and set attribute to preserve
    topology.defaults.attributes.interface.lag.id = 'int'
    topology.defaults.attributes.interface.lag.mclag = 'bool'
    topology.defaults.attributes.link.isl = 'bool'
    topology.defaults.attributes.node.mclagcluster = None
    topology.defaults.vlan.attributes.phy_ifattr.lag = None
    return


def post_transform(topology: Box) -> None:
    print('LAG PLUGIN POST_TRANSFORM')
    for n, ndata in topology.nodes.items():
        nodelags = {
                }
        for iface in ndata.interfaces:
            if 'lag' in iface and 'id' in iface.lag:
                lag_id_str = str(iface.lag.id)
                is_mclag = False
                if 'mclag' in iface.lag and iface.lag.mclag:
                    is_mclag = True
                if not lag_id_str in nodelags:
                    nodelags[lag_id_str] = {
                            'iflist': [ iface.ifname ],
                            'ifdata': iface,
                            'is_mclag': is_mclag,
                            }
                else:
                    nodelags[lag_id_str]['iflist'].append(iface.ifname)
        if nodelags:
            lagarray = []
            for lagid, lagdata in nodelags.items():
                lagdata['lag_id'] = lagid
                lagarray.append(lagdata)
            ndata.lags = lagarray

    return

