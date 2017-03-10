"""The functions in this module parse JSON inputs from an Xcessiv notebook"""
from __future__ import absolute_import, print_function,\
    nested_scopes, generators, division, with_statement, unicode_literals
from sklearn.model_selection import train_test_split
from xcessiv.functions import import_object_from_string_code


def return_train_data_from_json(input_json):
    """Returns train data set from input JSON

    Args:
        input_json (dict): "Extraction" dictionary

    Returns:
        X (numpy.ndarray): Features

        y (numpy.ndarray): Labels
    """
    extraction_code = "".join(input_json['main_dataset']["source"])
    extraction_function = import_object_from_string_code(extraction_code,
                                                         "extract_main_dataset")

    X, y = extraction_function()

    if input_json['test_dataset']['method'] == 'split_from_main':
        X, X_test, y, y_test = train_test_split(
            X,
            y,
            test_size=input_json['test_dataset']['split_ratio'],
            random_state=input_json['test_dataset']['split_seed'],
            stratify=y
        )

    if input_json['meta_feature_generation']['method'] == 'blend_split':
        X, X_test, y, y_test = train_test_split(
            X,
            y,
            test_size=input_json['meta_feature_generation']['split_ratio'],
            random_state=input_json['meta_feature_generation']['seed'],
            stratify=y
        )

    return X, y