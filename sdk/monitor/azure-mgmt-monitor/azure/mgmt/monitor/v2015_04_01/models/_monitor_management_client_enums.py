# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from six import with_metaclass
from azure.core import CaseInsensitiveEnumMeta


class ComparisonOperationType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """the operator that is used to compare the metric data and the threshold.
    """

    EQUALS = "Equals"
    NOT_EQUALS = "NotEquals"
    GREATER_THAN = "GreaterThan"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    LESS_THAN = "LessThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"

class ConditionOperator(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Operators allowed in the rule condition.
    """

    GREATER_THAN = "GreaterThan"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    LESS_THAN = "LessThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"

class EventLevel(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """the event level
    """

    CRITICAL = "Critical"
    ERROR = "Error"
    WARNING = "Warning"
    INFORMATIONAL = "Informational"
    VERBOSE = "Verbose"

class MetricStatisticType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """the metric statistic type. How the metrics from multiple instances are combined.
    """

    AVERAGE = "Average"
    MIN = "Min"
    MAX = "Max"
    SUM = "Sum"
    COUNT = "Count"

class RecurrenceFrequency(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """the recurrence frequency. How often the schedule profile should take effect. This value must be
    Week, meaning each week will have the same set of profiles. For example, to set a daily
    schedule, set **schedule** to every day of the week. The frequency property specifies that the
    schedule is repeated weekly.
    """

    NONE = "None"
    SECOND = "Second"
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"
    YEAR = "Year"

class ScaleDirection(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """the scale direction. Whether the scaling action increases or decreases the number of instances.
    """

    NONE = "None"
    INCREASE = "Increase"
    DECREASE = "Decrease"

class ScaleRuleMetricDimensionOperationType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """the dimension operator. Only 'Equals' and 'NotEquals' are supported. 'Equals' being equal to
    any of the values. 'NotEquals' being not equal to all of the values
    """

    EQUALS = "Equals"
    NOT_EQUALS = "NotEquals"

class ScaleType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """the type of action that should occur when the scale rule fires.
    """

    CHANGE_COUNT = "ChangeCount"
    PERCENT_CHANGE_COUNT = "PercentChangeCount"
    EXACT_COUNT = "ExactCount"
    SERVICE_ALLOWED_NEXT_VALUE = "ServiceAllowedNextValue"

class TimeAggregationOperator(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Aggregation operators allowed in a rule.
    """

    AVERAGE = "Average"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"
    LAST = "Last"

class TimeAggregationType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """time aggregation type. How the data that is collected should be combined over time. The default
    value is Average.
    """

    AVERAGE = "Average"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"
    COUNT = "Count"
    LAST = "Last"
