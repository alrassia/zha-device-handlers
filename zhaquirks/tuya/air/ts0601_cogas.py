from zigpy.profiles import zgp, zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import Basic, GreenPowerProxy, Groups, Ota, Scenes, Time

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya.air import (
    TuyaAirQualityCarbonMonoxide,
    TuyaAirQualityMethane,
    TuyaCarbonMonoxideDetectorZone,
    TuyaMethaneDetectorZone,
    TuyaMethaneManufCluster,
)


class CoMethaneSensor(CustomDevice):
    """Smart Gas&CO custom device implementation."""

    signature = {
        # "node_descriptor": "NodeDescriptor(logical_type=<LogicalType.Router: 1>, complex_descriptor_available=0, user_descriptor_available=0, reserved=0, aps_flags=0, frequency_band=<FrequencyBand.Freq2400MHz: 8>, mac_capability_flags=<MACCapabilityFlags.FullFunctionDevice|MainsPowered|RxOnWhenIdle|AllocateAddress: 142>, manufacturer_code=4417, maximum_buffer_size=66, maximum_incoming_transfer_size=66, server_mask=10752, maximum_outgoing_transfer_size=66, descriptor_capability_field=<DescriptorCapability.NONE: 0>, *allocate_address=True, *is_alternate_pan_coordinator=False, *is_coordinator=False, *is_end_device=False, *is_full_function_device=True, *is_mains_powered=True, *is_receiver_on_when_idle=True, *is_router=True, *is_security_capable=False)",
        # device_version=1
        # input_clusters=[0, 4, 5, 1036, 1037, 1280, 61184]
        # output_clusters=[10, 25]>
        MODELS_INFO: [("_TZE200_iuk8kupi", "TS0601")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TuyaMethaneManufCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TuyaMethaneManufCluster,
                    TuyaAirQualityCarbonMonoxide,
                    TuyaCarbonMonoxideDetectorZone,
                    TuyaAirQualityMethane,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.IAS_ZONE,
                INPUT_CLUSTERS: [TuyaMethaneDetectorZone],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,
                ],
            },
        },
    }
