from functools import partial
from multiprocessing import Pool

import numpy as np

from lauscher.abstract import Transformation
from lauscher.firing_probability import FiringProbability
from lauscher.helpers import CommandLineArguments
from lauscher.membranevelocity import MembraneVelocity


class HairCell(Transformation):
    # Model parameters have well-defined short names
    # pylint: disable=invalid-name
    def __init__(self, args):
        # Signature is given by model parameters
        # pylint: disable=too-many-arguments

        super().__init__()
        self.y = args.hc_y
        self.g = args.hc_g
        self.l = args.hc_l
        self.r = args.hc_r
        self.x = args.hc_x
        self.a = args.hc_a
        self.b = args.hc_b
        self.h = args.hc_h
        self.m = args.hc_m

    def _meddis(self, bm, fs):
        # Equation length is given by the model.
        # fs = sample rate
        # pylint: disable=too-many-locals

        # initialize inner hair cells
        ymdt = self.y * self.m / float(fs)
        xdt = self.x / float(fs)
        ydt = self.y / float(fs)
        rdt = self.r / float(fs)
        gdt = self.g / float(fs)
        hdt = self.h / float(fs)
        lplusrdt = (self.l + self.r) / float(fs)

        kt = self.g * self.a / (self.a + self.b)
        hair_c = self.m * self.y * kt / (self.l
                                         * kt + self.y * (self.l + self.r))
        hair_q = hair_c * (self.l + self.r) / kt
        hair_w = hair_c * self.r / self.x

        hc = np.zeros((bm.size))
        for j in range(bm.size):
            if (bm[j] + self.a) > 0:
                kt = gdt * (bm[j] + self.a) / (bm[j] + self.a + self.b)
            else:
                kt = 0.0

            if hair_q < self.m:
                replenish = ymdt - ydt * hair_q
            else:
                replenish = 0.0

            eject = kt * hair_q
            reuptakeandloss = lplusrdt * hair_c
            reuptake = rdt * hair_c
            reprocess = xdt * hair_w

            hair_q = np.max([hair_q + replenish - eject + reprocess, 0])
            hair_c = np.max([hair_c + eject - reuptakeandloss, 0])
            hair_w = np.max([hair_w + reuptake - reprocess, 0])

            hc[j] = hair_c * hdt
        return hc

    def __call__(self, data: MembraneVelocity) -> FiringProbability:
        """
        Calculate transmitter pool-based hair cell model

        References:
        Meddis, R. (March 1986). Simulation of mechanical to neural
        transduction in the auditory receptor. The Journal of the Acoustical
        Society of America. 79(3) 702
        Meddis, R. (March 1988). Simulation of auditory-neural transduction:
        Further studies. The Journal of the Acoustical Society of America.
        83(3) 1056
        """
        assert isinstance(data, MembraneVelocity)

        with Pool(CommandLineArguments().num_concurrent_jobs) as workers:
            samples = workers.map(partial(self._meddis, fs=data.sample_rate),
                                  data.channels)

        return FiringProbability(samples, data.sample_rate)
