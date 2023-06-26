from lauscher.abstract import Transformation
from lauscher.audiowaves import MonoAudioWave
from lauscher.spike_train import SpikeTrain
from lauscher.transformations import RmsNormalizer, HanningWindow, \
    BasilarMembrane, HairCell, BushyCell


class Wave2Spike(Transformation):
    def __init__(self,
                 args,
                 num_channels: int):
        self.num_channels = num_channels
        self.args = args

    def __call__(self, wave: MonoAudioWave) -> SpikeTrain:
        # noinspection PyTypeChecker
        return wave \
            .transform(RmsNormalizer(0.3)) \
            .transform(HanningWindow()) \
            .transform(BasilarMembrane(args=self.args, channels=self.num_channels)) \
            .transform(HairCell(args=self.args)) \
            .transform(BushyCell(args=self.args))
