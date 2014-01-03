"""Preprocessing functions for a single appliance / mains / circuit DataFrame"""

from __future__ import print_function, division
import numpy as np
import pandas as pd
from copy import deepcopy

def insert_zeros(single_appliance_dataframe, max_sample_period=None):
    """Some individual appliance monitors (IAM) get turned off occasionally.
    This might happen, for example, in the case where a hoover's IAM is 
    permanently attached to the hoover's power cord, even when the hoover is
    put away in the cupboard.

    Say the hoover was switched on and then both the hoover and the hoover's IAM
    were unplugged.  This would result in the dataset having a gap immediately
    after the on-segment.  This combination of an on-segment followed (without
    any zeros) by a gap might confuse downstream statistics and
    disaggregation functions.

    If, after any reading > 0, there is a gap in the dataset of more than 
    `max_sample_period` seconds then assume the appliance (and 
    individual appliance monitor) have been turned off from the
    mains and hence insert a zero max_sample_period seconds after 
    the last sample of the on-segment.

    TODO: a smarter version of this function might use information from
    the aggregate data to do a better job of estimating exactly when
    the appliance was turned off.

    Parameters
    ----------
    single_appliance_dataframe : pandas.DataFrame
        A DataFrame storing data from a single appliance

    max_sample_period : float or int, optional
        The maximum sample permissible period (in seconds). Any gap longer
        than `max_sample_period` is assumed to mean that the IAM 
        and appliance are off.  If None then will default to
        3 x the sample period of `single_appliance_dataframe`.

    Returns
    -------
    df_with_zeros : pandas.DataFrame
        A copy of `single_appliance_dataframe` with zeros inserted 
        `max_sample_period` seconds after the last sample of the on-segment.
    
    """
    # TODO: handle DataFrame

    df_with_zeros = deepcopy(single_appliance_dataframe)

    timedeltas = np.diff(df_with_zeros.index.values) / np.timedelta64(1, 's')
    readings_before_gaps = df_with_zeros[:-1][timedeltas > max_sample_period]
    # we only add a 0 if the preceeding value is > 0
    readings_before_gaps = readings_before_gaps[readings_before_gaps > 0]
    
    zeros = pd.Series(0,
                      index=readings_before_gaps.index +
                      pd.DateOffset(seconds=max_sample_period))
    df_with_zeros = df_with_zeros.append(zeros)
    df_with_zeros = df_with_zeros.sort_index()

    return df_with_zeros


def replace_nans_with_zeros(multiple_appliances_dataframe, max_sample_period):
    """For a single column, find gaps of > max_sample_period and replace
    all NaNs in these gaps with zeros.  But leave NaNs is gaps <=
    max_sample_period."""
    raise NotImplementedError
