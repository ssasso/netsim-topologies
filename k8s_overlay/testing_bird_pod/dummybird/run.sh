#!/bin/bash

h=$(hostname)

# Adding new dummy
ip link add dummy1 type dummy
ip link set up dev dummy1

echo "HELLO THERE!"
echo
echo "You can enter this console with:"
echo "  $ kubectl exec -it ${h} -- /bin/bash"
echo 

echo "Trying to work on net1 interface:"
ip addr sh dev net1

if [ $? -gt 0 ]; then
	echo "Device net1 not found... Sleeping and exiting."
	sleep 60
	exit 1
fi

NET1ADDR=$(/sbin/ifconfig net1 | grep 'inet addr:' | cut -d: -f2| cut -d' ' -f1)
LAST_OCTET=$(echo $NET1ADDR | cut -d'.' -f4)

: "${BASENET:=10.255.255}"

NEWIP="${BASENET}.${LAST_OCTET}"

echo "Auto-Calculated IP for additional dummy: $NEWIP"

ip addr add ${NEWIP}/32 dev dummy1

: "${PEERS:=10.150.150.1:65000}"
: "${BGPAS:=65100}"

# BGP Peers are taken from here
IFS=',' read -r -a bgp_list <<< "$PEERS"


echo > /etc/bird.conf
cat <<EOT >> /etc/bird.conf

router id ${NET1ADDR};

protocol kernel {
    scan time 5;
    learn;
    merge paths yes;
    persist yes;

    ipv4 {
        import all;
        export where source ~ [ RTS_STATIC, RTS_BGP ];
    };
}

protocol device dvc {
    scan time 5;
    interface "net*";
    interface "eth*";
    interface "dummy*";
}

protocol direct {
    ipv4 {
        import all;
    };
}

filter Export_DUMMY
{
    if ( net = ${NEWIP}/32 ) then accept;
    reject;
};

template bgp tpl_bgp {
    local as ${BGPAS};
    ipv4 {
        import all;
        export filter Export_DUMMY;
    };
}

EOT



cat <<EOT >> /etc/bird.conf
EOT

for peer in "${bgp_list[@]}"; do
    echo "  - need to add BGP Peer ${peer}"
    peerip=$(echo $peer | cut -d':' -f 1)
    peeras=$(echo $peer | cut -d':' -f 2)
cat <<EOT >> /etc/bird.conf

protocol bgp from tpl_bgp
{
    neighbor ${peerip} as ${peeras};
}

EOT
done


bird -f || e=1
while true; do
	sleep 600
done


