from converter.Exporter import Exporter
from converter.Loader import Loader
from converter.fnis.FNISBehavior import FNISBehavior
from converter.slal.SLALPack import SLALPack
from converter.slal.SLALRepairer import SLALRepairer
from converter.fnis.FNISParser import FNISParser
from converter.slsb.SLSBRepairer import SLSBRepairer


class SLALPackConverter:

    def start(dir):
        pack = SLALPack(dir)
        if not pack.validate():
            print(f"Pack {pack.toString()} | failed validation")
            return;

        pack.setup()

        Loader.load(pack)
            
        SLALRepairer.repair(pack)

        Exporter.convert_slal_to_slsb(pack)

        FNISParser.convert(pack)

        Loader.load_SLSBs(pack)

        SLSBRepairer().repair(pack)

        Exporter.export_corrected_slsbs(pack)

        FNISBehavior.build(pack)

        print(f"Pack {pack.toString()} | Done")