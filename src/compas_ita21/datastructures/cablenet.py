from compas.datastructures import Network


class Cablenet(Network):
    
    def __init__(self, *args, **kwargs):
        super(Cablenet, self).__init__(*args, **kwargs)
        self.default_node_attributes.update({
            'is_anchor': False,
            'residual': None,
            'px': 0,
            'py': 0,
            'pz': 0,
        })
        self.default_edge_attributes.update({
            'qpre': 1.0,
            'fpre': 0.0,
        })
