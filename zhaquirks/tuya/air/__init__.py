"""Tuya Air sensors."""

from typing import Any, Dict

import zigpy.types as t
from zigpy.zcl.clusters.measurement import (
    PM25,
    CarbonDioxideConcentration,
    CarbonMonoxideConcentration,
    FormaldehydeConcentration,
    RelativeHumidity,
    TemperatureMeasurement,
)
from zigpy.zcl.clusters.security import IasZone

from zhaquirks.tuya import DPToAttributeMapping, TuyaLocalCluster, TuyaNewManufCluster
from zhaquirks.tuya.mcu import TuyaMCUCluster

ZONE_TYPE = 0x0001


class TuyaAirQualityVOC(TuyaLocalCluster):
    """Tuya VOC level cluster."""

    cluster_id = 0x042E
    name = "VOC Level"
    ep_attribute = "voc_level"

    attributes = {
        0x0000: ("measured_value", t.Single),  # fraction of 1 (one)
        0x0001: ("min_measured_value", t.Single),
        0x0002: ("max_measured_value", t.Single),
        0x0003: ("tolerance", t.Single),
    }

    server_commands = {}
    client_commands = {}


class CustomTemperature(t.Struct):
    """Custom temperature wrapper."""

    field_1: t.int16s_be
    temperature: t.int16s_be

    @classmethod
    def from_value(cls, value):
        """Convert from a raw value to a Struct data."""
        return cls.deserialize(value.serialize())[0]


class TuyaAirQualityTemperature(TemperatureMeasurement, TuyaLocalCluster):
    """Tuya temperature measurement."""

    attributes = TemperatureMeasurement.attributes.copy()
    attributes.update(
        {
            # ramdom attribute IDs
            0xEF12: ("custom_temperature", CustomTemperature, False),
        }
    )

    def update_attribute(self, attr_name: str, value: Any) -> None:
        """Calculate the current temperature."""

        super().update_attribute(attr_name, value)

        if attr_name == "custom_temperature":
            super().update_attribute("measured_value", value.temperature * 10)


class TuyaAirQualityHumidity(RelativeHumidity, TuyaLocalCluster):
    """Tuya relative humidity measurement."""


class TuyaAirQualityPM25(PM25, TuyaLocalCluster):
    """Tuya PM25 concentration measurement"""


class TuyaAirQualityCO2(CarbonDioxideConcentration, TuyaLocalCluster):
    """Tuya Carbon Dioxide concentration measurement."""


class TuyaAirQualityCarbonMonoxide(CarbonMonoxideConcentration, TuyaLocalCluster):
    """Tuya Carbon Monoxide concentration measurement."""


class TuyaAirQualityFormaldehyde(FormaldehydeConcentration, TuyaLocalCluster):
    """Tuya Formaldehyde concentration measurement."""


class TuyaAirQualityMethane(CarbonDioxideConcentration, TuyaLocalCluster):
    """Tuya MethaneConcentration measurement."""


class TuyaCarbonMonoxideDetectorZone(IasZone, TuyaLocalCluster):
    """IAS Zone."""

    _CONSTANT_ATTRIBUTES = {ZONE_TYPE: IasZone.ZoneType.Carbon_Monoxide_Sensor}


class TuyaMethaneDetectorZone(IasZone, TuyaLocalCluster):
    """IAS Zone."""

    _CONSTANT_ATTRIBUTES = {
        ZONE_TYPE: IasZone.ZoneType.Carbon_Monoxide_Sensor
    }  # same type as used in TS0601_gas


class TuyaCO2ManufCluster(TuyaNewManufCluster):
    """Tuya with Air quality data points."""

    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        2: DPToAttributeMapping(
            TuyaAirQualityCO2.ep_attribute,
            "measured_value",
            lambda x: x * 1e-6,
        ),
        18: DPToAttributeMapping(
            TuyaAirQualityTemperature.ep_attribute,
            "custom_temperature",
            lambda x: CustomTemperature.from_value(x),
        ),
        19: DPToAttributeMapping(
            TuyaAirQualityHumidity.ep_attribute, "measured_value", lambda x: x * 10
        ),
        20: DPToAttributeMapping(
            TuyaAirQualityPM25.ep_attribute, "measured_value", lambda x: x
        ),
        21: DPToAttributeMapping(
            TuyaAirQualityVOC.ep_attribute, "measured_value", lambda x: x * 1e-6
        ),
        22: DPToAttributeMapping(
            TuyaAirQualityFormaldehyde.ep_attribute,
            "measured_value",
            lambda x: x * 1e-6,
        ),
    }

    data_point_handlers = {
        2: "_dp_2_attr_update",
        18: "_dp_2_attr_update",
        19: "_dp_2_attr_update",
        20: "_dp_2_attr_update",
        21: "_dp_2_attr_update",
        22: "_dp_2_attr_update",
    }


class TuyaMethaneManufCluster(TuyaMCUCluster):
    attributes = TuyaMCUCluster.attributes.copy()

    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        1: DPToAttributeMapping(
            TuyaMethaneDetectorZone.ep_attribute,
            "zone_status",
            lambda x: IasZone.ZoneStatus.Alarm_1 if not x else 0,
            endpoint_id=2,
        ),
        2: DPToAttributeMapping(
            TuyaAirQualityMethane.ep_attribute, "measured_value", lambda x: x * 1e-5
        ),
        18: DPToAttributeMapping(
            TuyaCarbonMonoxideDetectorZone.ep_attribute,
            "zone_status",
            lambda x: IasZone.ZoneStatus.Alarm_1 if not x else 0,
        ),
        19: DPToAttributeMapping(
            TuyaAirQualityCarbonMonoxide.ep_attribute,
            "measured_value",
            lambda x: x * 1e-8,
        ),
    }

    data_point_handlers = {
        1: "_dp_2_attr_update",
        2: "_dp_2_attr_update",
        18: "_dp_2_attr_update",
        19: "_dp_2_attr_update",
    }
