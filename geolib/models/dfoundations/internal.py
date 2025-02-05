import logging
from enum import IntEnum
from inspect import cleandoc

from pydantic import Field, StringConstraints
from pydantic.types import PositiveInt
from typing_extensions import Annotated

from geolib.models import BaseDataClass
from geolib.models.dseries_parser import (
    DSeriesInlineMappedProperties,
    DSeriesInlineProperties,
    DSeriesNoParseSubStructure,
    DSeriesStructure,
    DSeriesStructureCollection,
    DSeriesTreeStructure,
    DSeriesTreeStructureCollection,
    DSerieVersion,
)
from geolib.models.internal import Bool
from geolib.utils import make_newline_validator

from .dfoundations_structures import (
    DFoundationsCPTCollectionWrapper,
    DFoundationsEnumStructure,
    DFoundationsInlineProperties,
    DFoundationsTableWrapper,
)
from .internal_soil import Soil

logger = logging.getLogger(__name__)


UNKNOWN = "Unknown"
REQ_RUN_LINES = 6


class PileType(IntEnum):
    PREFABRICATED_CONCRETE_PILE = 0
    CLOSED_ENDED_STEEL_PIPE_PILE = 1
    DRIVEN_CAST_IN_PLACE_PILE_TUBE_BACK_BY_DRIVING = 2
    DRIVEN_CAST_IN_PLACE_PILE_TUBE_BACK_BY_VIBRATION = 3
    TAPERED_TIMBER_PILE = 4
    STRAIGHT_TIMBER_PILE = 5
    SCREW_PILE_CAST_IN_PLACE_LOST_TIP = 6
    SCREW_PILE_CAST_IN_PLACE_WITH_GROUT = 7
    PREFABRICATED_SCREW_PILE_WITH_GROUT = 8
    PREFABRICATED_SCREW_PILE_WITHOUT_GROUT = 9
    STEEL_SECTION = 10
    CONTINUOUS_FLIGHT_AUGER_PILE = 11
    BORED_PILE_DRILLING_MUD_UNCASED_BOREHOLE = 12
    BORED_PILE_SHELLING_TECH_PERMANENT_CASING = 13
    OPEN_ENDED_STEEL_PIPE_PILE = 14
    MV_PILE = 15
    MICRO_PILE_DOUBLE_PIPE_EXTORTED = 16
    MICRO_PILE_DOUBLE_PIPE_NOT_EXTORTED = 17
    MICRO_PILE_SINGLE_PIPE_EXTORTED = 18
    MICRO_PILE_SINGLE_PIPE_NOT_EXTORTED = 19
    MICRO_PILE_ANCHOR_BORED = 20
    MICRO_PILE_ANCHOR_SCREWED = 21
    MICRO_PILE_VIBRATED = 22
    GROUTED_STEEL_PROFILE_WITH_FOOTPLATE = 23
    GROUTED_STEEL_PIPE_PILE_SCREWED = 24
    USER_DEFINED_VIBRATING = 25
    USER_DEFINED_LOW_VIBRATING = 26
    USER_DEFINED = 27


class PileTypeForClayLoamPeat(IntEnum):
    STANDARD = 0
    USER_DEFINED = 1


class LoadSettlementCurve(IntEnum):
    ONE = 0
    TWO = 1
    THREE = 2


class PileMaterial(IntEnum):
    CONCRETE = 0
    STEEL = 1
    TIMBER = 2
    USER_DEFINED = 3


class BearingPileSlipLayer(IntEnum):
    NONE = 0
    SYNTHETIC = 1
    BENTONITE = 2
    BITUMEN = 3
    USER_DEFINED = 4


class PileShape(IntEnum):
    ROUND_PILE = 0
    RECTANGULAR_PILE = 1
    ROUND_PILE_WITH_ENLARGED_BASE = 2
    RECTANGULAR_PILE_WITH_ENLARGED_BASE = 3
    ROUND_TAPERED_PILE = 4
    ROUND_HOLLOW_PILE_WITH_CLOSED_BASE = 5
    ROUND_PILE_WITH_LOST_TIP = 6
    ROUND_PILE_WITH_IN_SITU_FORMED_BASE = 7
    SECTION = 8
    ROUND_OPEN_ENDED_HOLLOW_PILE = 9
    H_SHAPED_PROFILE = 10
    USER_DEFINED = 11


class TypesBearingPiles(DSeriesNoParseSubStructure):
    pile_name: str = ""
    pile_type: PileType = PileType.PREFABRICATED_CONCRETE_PILE
    pile_type_for_execution_factor_sand_gravel: PileType | None = None
    execution_factor_sand_gravel: Annotated[float, Field(ge=0, le=9)] | None = None
    pile_type_for_execution_factor_clay_loam_peat: PileTypeForClayLoamPeat | None = None
    execution_factor_clay_loam_peat: Annotated[float, Field(ge=0, le=9)] | None = None
    pile_type_for_pile_class_factor: PileType | None = None
    pile_class_factor: Annotated[float, Field(ge=0, le=9)] | None = None
    pile_type_for_load_settlement_curve: LoadSettlementCurve | None = None
    material: PileMaterial | None = None
    elasticity_modulus: Annotated[float, Field(ge=0, le=1e25)] | None = None
    slip_layer: BearingPileSlipLayer = BearingPileSlipLayer.NONE
    characteristic_adhesion: Annotated[float, Field(ge=0, le=1000)] | None = None
    shape: PileShape = PileShape.RECTANGULAR_PILE
    base_width: Annotated[float, Field(ge=0, le=100)] | None = None
    base_length: Annotated[float, Field(ge=0, le=100)] | None = None
    diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    base_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    pile_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    base_height: Annotated[float, Field(ge=0, le=100)] | None = None
    base_width_v: Annotated[float, Field(ge=0, le=100)] | None = None
    base_length_v: Annotated[float, Field(ge=0, le=100)] | None = None
    shaft_width: Annotated[float, Field(ge=0, le=100)] | None = None
    shaft_length: Annotated[float, Field(ge=0, le=100)] | None = None
    increase_in_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    external_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    internal_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    height_h_shape: Annotated[float, Field(ge=0, le=100)] | None = None
    width_h_shape: Annotated[float, Field(ge=0, le=100)] | None = None
    thickness_web: Annotated[float, Field(ge=0, le=100)] | None = None
    thickness_flange: Annotated[float, Field(ge=0, le=100)] | None = None
    overrule_pile_tip_shape_factor: Bool = Bool.FALSE
    pile_tip_shape_factor: Annotated[float, Field(ge=0, le=10)] | None = None
    overrule_pile_tip_cross_section_factors: Bool = Bool.FALSE
    pile_tip_cross_section_factor: Annotated[float, Field(ge=0, le=10)] | None = None
    use_pre_2016: Bool = Bool.FALSE
    user_defined_pile_type_as_prefab: Bool = Bool.FALSE
    use_manual_reduction_for_qc: Bool = Bool.FALSE
    reduction_percentage_qc: Annotated[float, Field(ge=25, le=100)] = 25
    is_user_defined: Bool = Bool.TRUE


class TypesTensionPiles(DSeriesNoParseSubStructure):
    pile_name: str = ""
    pile_type: PileType = PileType.PREFABRICATED_CONCRETE_PILE
    pile_type_for_execution_factor_sand_gravel: PileType | None = None
    execution_factor_sand_gravel: Annotated[float, Field(ge=0, le=9)] | None = None
    pile_type_for_execution_factor_clay_loam_peat: PileTypeForClayLoamPeat | None = None
    execution_factor_clay_loam_peat: Annotated[float, Field(ge=0, le=9)] | None = None
    material: PileMaterial | None = None
    unit_weight_pile: Annotated[float, Field(ge=0, le=1000)] | None = None
    elasticity_modulus: Annotated[float, Field(ge=0, le=1e25)] | None = None
    shape: PileShape = PileShape.RECTANGULAR_PILE
    base_width: Annotated[float, Field(ge=0, le=100)] | None = None
    base_length: Annotated[float, Field(ge=0, le=100)] | None = None
    diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    base_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    pile_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    base_height: Annotated[float, Field(ge=0, le=100)] | None = None
    base_width_v: Annotated[float, Field(ge=0, le=100)] | None = None
    base_length_v: Annotated[float, Field(ge=0, le=100)] | None = None
    shaft_width: Annotated[float, Field(ge=0, le=100)] | None = None
    shaft_length: Annotated[float, Field(ge=0, le=100)] | None = None
    increase_in_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    external_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    internal_diameter: Annotated[float, Field(ge=0, le=100)] | None = None
    height_h_shape: Annotated[float, Field(ge=0, le=100)] | None = None
    width_h_shape: Annotated[float, Field(ge=0, le=100)] | None = None
    thickness_web: Annotated[float, Field(ge=0, le=100)] | None = None
    thickness_flange: Annotated[float, Field(ge=0, le=100)] | None = None
    circumference: Annotated[float, Field(ge=0, le=100)] | None = None
    cross_section: Annotated[float, Field(ge=0, le=100)] | None = None
    is_user_defined: Bool = Bool.TRUE


class SoilCollection(DSeriesStructureCollection):
    soil: list[Soil] = Soil.default_soils()

    def add_soil_if_unique(self, soil) -> None:
        for added_soil in self.soil:
            if soil.name == added_soil.name:
                raise NameError(f"Soil with name {soil.name} already exists.")
        self.soil.append(soil)
        return soil

    def find_soil_id(self, key) -> int:
        for i, soil in enumerate(self.soil):
            if soil.name == key:
                return i
        raise KeyError(f"Soil with {key} not present.")

    def __getitem__(self, key) -> Soil:
        if isinstance(key, int):
            return self.soil[key]
        elif isinstance(key, str):
            for soil in self.soil:
                if soil.name == key:
                    return soil
            raise KeyError(key)


class Layer(DSeriesTreeStructure):
    name: str = ""  # will be generated by template
    material: int
    top_level: float  # [m]
    excess_pore_pressure_top: float = 0.0  # [kN/m3]
    excess_pore_pressure_bottom: float = 0.0  # [kN/m3]
    ocr_value: float = 1.0  # [-]
    reduction_core_resistance: float = 0.0  # [%]


class ReductionCoreResistanceEnum(IntEnum):
    SAFE = 0
    BEGEMANN = 1
    MANUAL = 2


class Profile(DSeriesTreeStructure):
    name: str
    matching_cpt: int
    x_coordinate: float
    y_coordinate: float
    phreatic_level: float
    pile_tip_level: float
    overconsolidation_ratio: float = 1.0
    top_of_positive_skin_friction: float
    bottom_of_negative_skin_friction: float
    expected_ground_level_settlement: float = 0.0
    placement_depth_of_foundation: float = 0.0
    concentration_value_frohlich: int = 3
    top_tension_zone: float = 0.0

    # Excavation part
    reduction_of_core_resistance: ReductionCoreResistanceEnum = (
        ReductionCoreResistanceEnum.SAFE
    )
    excavation_level: float
    excavation_width_infinite: Bool = Bool.TRUE
    excavation_length_infinite: Bool = Bool.TRUE
    distance_edge_pile_to_excavation_boundary: float = 0.0  # only valid for BEGEMANN

    layers: list[Layer] = []


class Profiles(DSeriesTreeStructureCollection):
    profiles: list[Profile] = []

    def add_profile_if_unique(self, profile: Profile) -> Profile:
        for added_profile in self.profiles:
            added_profile.excavation_level = profile.excavation_level
            if profile.name == added_profile.name:
                raise NameError(f"profile with name {profile.name} already exists.")
        self.profiles.append(profile)
        return profile


class InternalPile(BaseDataClass):
    # Only share method here, as shared properties
    # will not be picked up by parsers/pydantic
    def __eq__(self, other):
        """Overrides the default implementation"""
        if self.pile_name == other.pile_name:
            Warning(
                "Pile with name: "
                + self.pile_name
                + " already exists, pile is not added."
            )
            return True
        else:
            return False


class PositionBearingPile(InternalPile):
    index: PositiveInt = 1
    x_coordinate: Annotated[float, Field(ge=-10000000, le=100000000)]
    y_coordinate: Annotated[float, Field(ge=-10000000, le=100000000)]
    pile_head_level: Annotated[float, Field(ge=-1000, le=1000)]
    surcharge: Annotated[float, Field(ge=0, le=100000)]
    limit_state_str: Annotated[float, Field(ge=0, le=100000)]
    limit_state_service: Annotated[float, Field(ge=0, le=100000)]
    pile_name: Annotated[str, StringConstraints(min_length=1, max_length=100)]


class PositionTensionPile(InternalPile):
    index: PositiveInt = 1
    x_coordinate: Annotated[float, Field(ge=-10000000, le=100000000)]
    y_coordinate: Annotated[float, Field(ge=-10000000, le=100000000)]
    pile_head_level: Annotated[float, Field(ge=-1000, le=1000)]
    use_alternating_loads: Bool
    max_force: Annotated[float, Field(ge=-100000, le=100000)]
    min_force: Annotated[float, Field(ge=-100000, le=100000)]
    limit_state_str: Annotated[float, Field(ge=0, le=100000)]
    limit_state_service: Annotated[float, Field(ge=0, le=100000)]
    pile_name: Annotated[str, StringConstraints(min_length=1, max_length=100)]


class PositionsBearingPiles(DSeriesNoParseSubStructure):
    positions: list[PositionBearingPile] = []


class PositionsTensionPiles(DSeriesNoParseSubStructure):
    positions: list[PositionTensionPile] = []


class CPTMeasureData(DFoundationsTableWrapper):
    data: list[dict[str, float]]


class ExcavationType(IntEnum):
    BEFORE = 1
    AFTER = 2


class TimeOrderType(IntEnum):
    """Use this option to specify the execution time of CPTs relative to the pile installation.
    This information is needed to determine whether the problem qualifies for certain exceptions made in NEN 9997-1:2016.

    """

    CPT_EXCAVATION_INSTALL = 1
    INSTALL_CPT_EXCAVATION = 2
    EXCAVATION_CPT_INSTALL = 3
    EXCAVATION_INSTALL_CPT = 4
    INSTALL_EXCAVATION_CPT = 5
    CPT_INSTALL_EXCAVATION = 6
    CPT_BEFORE_AND_AFTER_INSTALL = 7


class InterpretationType(IntEnum):
    NEN_RULE = 0
    CUR = 1
    THREE_TYPE_RULE = 2
    QC_ONLY = 3
    UNKNOWN = 4


class CPT(DFoundationsEnumStructure):
    cptname: str
    project_name: str = UNKNOWN
    projectid: str = ""
    project_number: str = ""
    project_subnumber: str = ""
    location_name: str = UNKNOWN
    client_name: str = UNKNOWN
    companyid: str = UNKNOWN
    filedate: str = ""
    fileowner: str = UNKNOWN
    gef_version: str = UNKNOWN
    procedurecode: str = UNKNOWN
    objectid: str = "0"
    startdate: str = ""
    starttime: str = ""
    excavation_type: ExcavationType  # 1 : Before
    timeorder_type: TimeOrderType  # 1 : CPT - Excavation - Install
    cpt_type: int = 1  # Electronic
    usage_cone_value: int = 0  # Mechanical qc required
    xy_coordinate_system: str = UNKNOWN
    xworld: float = 987654321.00000
    xworld_accuracy: float = 987654321.00000
    yworld: float = 987654321.00000
    yworld_accuracy: float = 987654321.00000
    groundlevel: float
    groundlevel_accuracy: float = 987654321.00000
    groundlevel_was_measured: Bool = Bool.FALSE
    leveltext: str = ""
    pre_excavation: float
    waterlevel: float = 987654321.000
    xlocal: float = 0.0
    ylocal: float = 0.0
    local_x_crosssection: float = 0.000
    interpretation_model: InterpretationType
    interpretation_model_stressdependent: Bool
    depthrange: float
    graph_max_percentage: int = 10
    graph_width: float = 10.0
    graph_linewidth: int = 1
    graph_borderwidth: int = 1
    graph_bordercolor: int = 0
    graph_frictioncolor: int = 16711680
    graph_qccolor: int = 255
    graph_plane_color: int = 0
    graph_fit_for_size: Bool = Bool.TRUE
    graph_fit_symbol_for_size: Bool = Bool.TRUE
    graph_symbol_size: float = 1.0
    void_value_depth: float = 987654321.000
    void_value_cone_resistance: float = 987654321.000
    void_value_pore_water_pressure: float = 987654321.000
    void_value_sleeve_friction: float = 987654321.000
    void_value_friction_number: float = 987654321.000
    void_value_equivalent_electronic_qc: float = 987000000.000000
    measured_data: CPTMeasureData


class CPTList(DFoundationsCPTCollectionWrapper):
    cpt_collection: list[CPT] = []

    def add_cpt(self, cpt: CPT):
        """Add CPT and return id.
        Forces timeordertype to be the same everywhere.
        """
        for existing_cpt in self.cpt_collection:
            existing_cpt.timeorder_type = cpt.timeorder_type
        self.cpt_collection.append(cpt)
        return len(self.cpt_collection) - 1

    def __getitem__(self, key) -> CPT:
        if isinstance(key, int):
            return self.cpt_collection[key]
        elif isinstance(key, str):
            for cpt in self.cpt_collection:
                if cpt.cptname == key:
                    return cpt
            raise KeyError(key)


class CalculationOptions(DSeriesNoParseSubStructure):
    # Rigidity of superstructure
    is_rigid: Bool = Bool.TRUE

    # Transformation
    max_allowed_settlement_lim_state_str: Annotated[float, Field(ge=0, le=100000)] = 0
    max_allowed_rel_rotation_lim_state_str: Annotated[int, Field(ge=1, le=10000)] = 100
    max_allowed_settlement_lim_state_serv: Annotated[float, Field(ge=0, le=100000)] = 0
    max_allowed_rel_rotation_lim_state_serv: Annotated[int, Field(ge=1, le=10000)] = 300

    # Overrule parameters Bearing Piles
    is_xi3_overruled: Bool = Bool.FALSE
    factor_xi3: Annotated[float, Field(ge=0.01, le=10)] | None = 2
    is_xi4_overruled: Bool = Bool.FALSE
    factor_xi4: Annotated[float, Field(ge=0.01, le=10)] | None = 2
    is_gamma_b_overruled: Bool = Bool.FALSE
    factor_gamma_b: Annotated[float, Field(ge=1, le=100)] | None = 2
    is_gamma_s_overruled: Bool = Bool.FALSE
    factor_gamma_s: Annotated[float, Field(ge=1, le=100)] | None = 2
    is_gamma_fnk_overruled: Bool = Bool.FALSE
    factor_gamma_fnk: Annotated[float, Field(ge=-100, le=100)] | None = 2
    is_area_overruled: Bool = Bool.FALSE
    area: Annotated[float, Field(ge=0, le=100000)] | None = 1000
    is_qbmax_overruled: Bool = Bool.FALSE
    qbmax: Annotated[float, Field(ge=0, le=100)] | None = 15
    is_qcza_low_overruled: Bool = Bool.FALSE
    qcza_low: Annotated[float, Field(ge=0, le=100)] | None = 12
    is_qcza_high_overruled: Bool = Bool.FALSE
    qcza_high: Annotated[float, Field(ge=0, le=100)] | None = 15
    is_ea_gem_overruled: Bool = Bool.FALSE
    ea_gem: Annotated[float, Field(ge=1)] | None = 100000

    # Model options combined
    is_suppress_qc_reduction: Bool = Bool.FALSE
    is_overrule_excavation: Bool = Bool.FALSE
    use_pile_group: Bool = Bool.TRUE
    is_write_intermediate_results: Bool = Bool.FALSE
    use_interaction_model: Bool = Bool.FALSE
    use_almere_rules: Bool = Bool.FALSE
    use_extra_almere_rules: Bool = Bool.FALSE

    # Overrule parameters Shallow foundations
    is_gamma_g_str_overruled: Bool = Bool.FALSE
    factor_gamma_g_str: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_coh_overruled: Bool = Bool.FALSE
    factor_gamma_coh: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_phi_overruled: Bool = Bool.FALSE
    factor_gamma_phi: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_fundr_overruled: Bool = Bool.FALSE
    factor_gamma_fundr: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_g_sls_overruled: Bool = Bool.FALSE
    factor_gamma_g_sls: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_cc_overruled: Bool = Bool.FALSE
    factor_gamma_cc: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_ca_overruled: Bool = Bool.FALSE
    factor_gamma_ca: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_keep_length_constant: Bool = Bool.FALSE
    use_5_percent_limit: Bool = Bool.FALSE
    load_factor_between_limit_1_and_2: Annotated[float, Field(ge=0.5, le=1)] = 0.833

    # Overrule parameters Tension Piles
    unit_weight_water: Annotated[float, Field(ge=0.01, le=20)] = 9.81
    use_compaction: Bool = Bool.FALSE
    is_gamma_var_overruled: Bool = Bool.FALSE
    factor_gamma_var: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_st_overruled: Bool = Bool.FALSE
    factor_gamma_st: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    is_gamma_gamma_overruled: Bool = Bool.FALSE
    factor_gamma_gamma: Annotated[float, Field(ge=0.01, le=100)] | None = 1.0
    surcharge: Annotated[float, Field(ge=0, le=1e7)] = 0
    use_piezometric_levels: Bool = Bool.TRUE

    def __init__(self, *args, **kwargs):
        """If defaults are overriden, update
        the related toggle fields as well.
        """
        toggles = {}
        for field, value in kwargs.items():
            if value is None:
                continue  # Nones will be passed by default settings
            toggle_field = self.find_toggle(field)
            fields = self.model_fields
            if toggle_field in fields:
                toggles[toggle_field] = Bool.TRUE
        kwargs.update(toggles)
        super().__init__(*args, **kwargs)

    @staticmethod
    def find_toggle(field):
        """Transform given field like `factor_gamma_s_bpb`
        into `is_gamma_s_bpb_overruled`.
        """
        return "is_" + field.replace("factor_", "") + "_overruled"


class ModelTypeEnum(IntEnum):
    BEARING_PILES = 0
    TENSION_PILES = 1
    SHALLOW_FOUNDATIONS = 2


class ModelType(DFoundationsInlineProperties):
    model: ModelTypeEnum = ModelTypeEnum.BEARING_PILES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We only support Bearing & Tension Piles (NL)
        if self.model >= 2:
            logger.error(f"Model Type {self.model} is unsupported!")


class MainCalculationType(IntEnum):
    PRELIMINARY_DESIGN = 0
    VERIFICATION_DESIGN = 1


class SubCalculationType(IntEnum):
    VERIFICATION_DESIGN = 0
    VERIFICATION_COMPLETE = 1
    INDICATION_BEARING_CAPACITY = 2
    BEARING_CAPACITY_AT_FIXED_PILETIP_LEVELS = 3
    PILETIP_LEVELS_AND_NET_BEARING_CAPACITY = 4
    UNSUPPORTED = 7


class CalculationType(DFoundationsInlineProperties):
    main_calculationtype: MainCalculationType = MainCalculationType.PRELIMINARY_DESIGN
    sub_calculationtype: SubCalculationType = (
        SubCalculationType.INDICATION_BEARING_CAPACITY
    )

    def __init__(self, *args, **kwargs):
        # Set maintype automatically based on subtype
        super().__init__(*args, **kwargs)
        if self.sub_calculationtype.value >= 2:
            self.main_calculationtype = MainCalculationType.PRELIMINARY_DESIGN
        else:
            self.main_calculationtype = MainCalculationType.VERIFICATION_DESIGN


class PreliminaryDesign(DSeriesNoParseSubStructure):
    trajectory_begin: float = -10.00
    trajectory_end: float = -25.00
    trajectory_interval: float = 0.50

    profiles: list[int] = []  # ids of Profiles
    # Can be single pile type only in case of verification
    pile_types: list[int] = []  # ids of Piles

    # Only valid for Verification Design
    cpt_test_level: float | None = 0.0  # [m]

    # Only valid for Prelimary Design
    net_bearing_capacity: int | None = 0  # [kN]


class Version(DSerieVersion):
    soil: int = 1010
    d__foundations: int = 1024


class VersionExternal(DSeriesInlineMappedProperties):
    dgsfoundationcalc____dll: str = "23.1.0.40358"


class DFoundationsInputStructure(DSeriesStructure):
    """Representation of complete .foi file."""

    version: Version = Version()
    version_externals: VersionExternal = VersionExternal()
    model: ModelType = ModelType()
    soil_collection: SoilCollection = SoilCollection()
    run_identification: str = 6 * "\n"
    cpt_list: CPTList = CPTList()
    profiles: Profiles = Profiles()
    user_classification_method: str = cleandoc(
        """          
        [USER CLASSIFICATION METHOD]
        0
        [END OF USER CLASSIFICATION METHOD]
        """
    )
    slopes: str = cleandoc(
        """
            0 = number of items
        """
    )
    types___bearing_piles: list[TypesBearingPiles] | str = cleandoc(
        """
        -1 : pile type shown in main graph
            0 = number of items
        """
    )
    types___tension_piles_cur: list[TypesTensionPiles] | str = cleandoc(
        """
        -1 : pile type shown in main graph
            0 = number of items
        """
    )
    types___shallow_foundations: str = cleandoc(
        """
            0 = number of items
        """
    )
    loads: str = cleandoc(
        """
            0 = number of items
        """
    )
    positions___bearing_piles: PositionsBearingPiles | str = PositionsBearingPiles()

    positions___tension_piles_cur: PositionsTensionPiles | str = PositionsTensionPiles()
    positions___shallow_foundations: str = cleandoc(
        """
        [TABLE]
        DataCount=0
        [END OF TABLE]
        """
    )
    calculation_options: CalculationOptions | str = CalculationOptions()
    calculationtype: CalculationType = CalculationType()
    preliminary_design: PreliminaryDesign | str = PreliminaryDesign()
    location_map: str = cleandoc(
        """
         0.0000
                0.0000
                0.0000
                0.0000
        """
    )

    # Custom validator
    _validate_run_identification = make_newline_validator(
        "run_identification", req_newlines=REQ_RUN_LINES
    )


class DFoundationsNenPileResultsTable(DFoundationsTableWrapper):
    data: list[dict[str, int | float | str]] = []


class DFoundationsCalculationParametersBearingPilesEC7(DSeriesInlineProperties):
    ksi3used: float
    ksi4used: float
    gammabused: float
    gammasused: float
    isksi3used: bool


# region VerificationResults


class DFoundationsNenPileResults(DFoundationsInlineProperties):
    cpts: DFoundationsNenPileResultsTable
    pile_point_shape_factor: float
    factor_influence_crosssection_of_pile_point_s: float
    max_load_on_foundation: float
    max_bearing_capacity_foundation: float
    critical_pile_nr_for_settlement_in_gt1b: int
    critical_cpt_nr_for_settlement_in_gt1b: int
    critical_pile_nr_for_settlement_in_gt2: int
    critical_cpt_nr_for_settlement_in_gt2: int
    first_pile_nr_for_critical_rotation_in_gt1b: int
    second_pile_nr_for_critical_rotation_in_gt1b: int
    first_pile_nr_for_critical_rotation_in_gt2: int
    second_pile_nr_for_critical_rotation_ingt2: int
    fs_tot_d_1b: float
    fr_max_punt_d_1b: float
    fr_max_schacht_d_1b: float
    fr_punt_d_1b: float
    spunt_d_1b: float
    sel_d1b: float
    s2_d1b: float
    sneg1b: float
    fs_tot_d_2: float
    fr_max_punt_d2: float
    fr_max_schacht_d_2: float
    fr_punt_d_2: float
    spunt_d_2: float
    sel_d2: float
    s2_d2: float
    sneg2: float
    max_shaft_and_point: DFoundationsNenPileResultsTable
    sigma_max_schacht_1b: float
    sigma_max_schacht_2: float
    min_value: float
    max_value: float
    nen_average_pile_factors: DFoundationsNenPileResultsTable
    calculation_parameters_bearing_piles_ec_7: (
        DFoundationsCalculationParametersBearingPilesEC7
    )

    @classmethod
    def header_lines(cls) -> int:
        """Tells to the parent class that this structure text comes
        with three lines of header text that can be skipped.

        Returns:
            int: Header line size.
        """
        return 3


class DFoundationsGlobalNenResults(DFoundationsInlineProperties):
    wd1b: float
    w2d: float
    reciprocal_max_relative_rotation_calc_1B: float
    reciprocal_max_relative_rotation_calc_2: float


class DFoundationsVerificationResults(DSeriesStructure):
    global_nen_results: DFoundationsGlobalNenResults | None = None
    demands_nen__en: str | None = None
    nen_pile_results: DFoundationsNenPileResults | None = None

    verification_results_tp_load__settlement_curve_1b: str | None = None
    verification_results_tp_1a: str | None = None
    verification_results_tp_1b2: str | None = None
    verification_results_tp_load__settlement_curve_2: str | None = None


# endregion


# region Output


class DFoundationsCalculationWarnings(DSeriesTreeStructure):
    is_warning_f1_given: Bool
    f1_greater_than_1_found: Bool
    is_warning_nen_depth_given: Bool
    is_warning_sf_fund_width_given: Bool
    is_warning_sf_fund_length_given: Bool
    is_warning_sf_cud_given: Bool
    is_warning_sf_delta_phi_given: Bool
    is_warning_nen_spacing_given: int = int()
    is_warning_sf_slope_not_relevant_given: Bool
    is_warning_nen_sf_placement_depth_too_deep: Bool
    is_warning_nen_sf_placement_depth_too_shallow: Bool
    is_warning_nen_bp_positive_skin_friction_zone_given: Bool
    is_warning_sf_foundation_level_for_punch_to_deep_for_slope_given: Bool


class DFoundationsDumpfileOutputStructure(DSeriesStructure):
    results_at_cpt_test_level: str | None = None
    verification_results: DFoundationsVerificationResults | None = None

    calculation_parameters_tension_piles: str | None = None
    verification_results_tp: DFoundationsVerificationResults | None = None

    footnote_warnings: str | None = None
    preliminary_design_results: str | None = None
    verification_results_sf: str | None = None
    verification_results_tp_1b2: str | None = None
    verification_design_results: str | None = None
    calculation_warnings: DFoundationsCalculationWarnings | None = None


class DFoundationsStructure(DSeriesStructure):
    input_data: DFoundationsInputStructure = DFoundationsInputStructure()
    dumpfile_output: DFoundationsDumpfileOutputStructure | None = None


class DFoundationsDumpStructure(DSeriesStructure):
    dumpfile: DFoundationsStructure = DFoundationsStructure()


# endregion
