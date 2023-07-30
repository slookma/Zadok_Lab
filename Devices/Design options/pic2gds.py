# -*- coding: utf-8 -*-

import nazca as nd
nd.image('logo4.PNG', threshold=0.4).put(400)
nd.image('logo4.PNG', threshold=0.6).put(800)
nd.image('logo4.PNG', threshold=0.8).put(1200)
nd.image('logo4.PNG', threshold=0.9).put(1600)

nd.export_gds()