# coding: utf-8

"""
Selection methods defining categories based on selection step results.
"""

from columnflow.util import maybe_import
from columnflow.selection import Selector, SelectionResult, selector

np = maybe_import("numpy")
ak = maybe_import("awkward")


@selector(uses={"event"})
def catid_selection_incl(self: Selector, events: ak.Array, **kwargs) -> ak.Array:
    return ak.ones_like(events.event) > 0


@selector(uses={"event"})
def catid_selection_1e(self: Selector, events: ak.Array, results: SelectionResult, **kwargs) -> ak.Array:
    return (ak.num(results.objects.Electron.Electron, axis=-1) == 1) & (ak.num(results.objects.Muon.Muon, axis=-1) == 0)


@selector(uses={"event"})
def catid_selection_1mu(self: Selector, events: ak.Array, results: SelectionResult, **kwargs) -> ak.Array:
    return (ak.num(results.objects.Electron.Electron, axis=-1) == 0) & (ak.num(results.objects.Muon.Muon, axis=-1) == 1)


@selector(uses={"Electron.pt", "Muon.pt"})
def catid_1e(self: Selector, events: ak.Array, **kwargs) -> ak.Array:
    return (ak.sum(events.Electron.pt > 0, axis=-1) == 1) & (ak.sum(events.Muon.pt > 0, axis=-1) == 0)


@selector(uses={"Electron.pt", "Muon.pt"})
def catid_1mu(self: Selector, events: ak.Array, **kwargs) -> ak.Array:
    return (ak.sum(events.Electron.pt > 0, axis=-1) == 0) & (ak.sum(events.Muon.pt > 0, axis=-1) == 1)


@selector(uses={"Jet.pt", "FatJet.pt"})
def catid_boosted(self: Selector, events: ak.Array, **kwargs) -> ak.Array:
    """
    Categorization of events in the boosted category: presence of at least 1 AK8 jet fulfilling
    requirements given by the Selector called in SelectEvents
    """
    return (ak.sum(events.Jet.pt > 0, axis=-1) >= 1) & (ak.sum(events.FatJet.pt > 0, axis=-1) >= 1)


@selector(uses={"Jet.pt", "FatJet.pt"})
def catid_resolved(self: Selector, events: ak.Array, **kwargs) -> ak.Array:
    """
    Categorization of events in the resolved category: presence of no AK8 jets fulfilling
    requirements given by the Selector called in SelectEvents
    """
    return (ak.sum(events.Jet.pt > 0, axis=-1) >= 3) & (ak.sum(events.FatJet.pt > 0, axis=-1) == 0)


@selector(uses={"Jet.btagDeepFlavB"})
def catid_1b(self: Selector, events: ak.Array, **kwargs) -> ak.Array:

    n_deepjet = ak.sum(events.Jet.btagDeepFlavB >= self.config_inst.x.btag_working_points.deepjet.medium, axis=-1)

    return (n_deepjet == 1)


@selector(uses={"Jet.btagDeepFlavB"})
def catid_2b(self: Selector, events: ak.Array, **kwargs) -> ak.Array:

    n_deepjet = ak.sum(events.Jet.btagDeepFlavB >= self.config_inst.x.btag_working_points.deepjet.medium, axis=-1)

    return (n_deepjet >= 2)


# TODO: not hard-coded -> use config!
ml_model_name = "dev"
ml_processes = ["ggHH_kl_1_kt_1_sl_hbbhww", "tt", "st", "w_lnu", "dy_lep"]
# TODO ml categories
for proc in ml_processes:
    @selector(
        uses=set(f"{ml_model_name}.score_{proc1}" for proc1 in ml_processes),
        cls_name=f"catid_ml_{proc}",
    )
    def dnn_mask(self: Selector, events: ak.Array, **kwargs) -> ak.Array:
        """
        dynamically built selector that categorizes events based on dnn scores
        """
        print("TODO: dnn_mask")

        raise NotImplementedError("TODO: dnn_mask")
