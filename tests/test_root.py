# -*- coding: utf-8 -*-
# Copyright 2024 Matthew Fitzpatrick.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
r"""Contains tests for the module :mod:`czekitout.convert`.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For performing deep copies.
import copy

# For operations related to unit tests.
import pytest

# For removing files.
import pathlib



# For validating and converting objects.
import czekitout.check
import czekitout.convert



# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



##################################
## Define classes and functions ##
##################################



def check_and_convert_slice_obj(params):
    obj_name = "slice_obj"
    kwargs = {"obj": params[obj_name],
              "obj_name": obj_name,
              "accepted_types": (slice,)}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)
    slice_obj = copy.deepcopy(params[obj_name])

    return slice_obj



def check_and_convert_seed(params):
    obj_name = "seed"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    seed = czekitout.convert.to_nonnegative_int(**kwargs)

    return seed



def pre_serialize_slice_obj(slice_obj):
    serializable_rep = {"start": slice_obj.start, 
                        "stop": slice_obj.stop, 
                        "step": slice_obj.step}
    
    return serializable_rep



def pre_serialize_seed(seed):
    serializable_rep = seed
    
    return serializable_rep




def de_pre_serialize_slice_obj(serializable_rep):
    slice_obj = slice(serializable_rep["start"], 
                      serializable_rep["stop"], 
                      serializable_rep["step"])
    
    return slice_obj



def de_pre_serialize_seed(serializable_rep):
    seed = serializable_rep
    
    return seed



def test_1_of_PreSerializableAndUpdatable():
    slice_obj_1 = slice(None, 6, 1)
    slice_obj_2 = slice(3, None, 1)

    validation_and_conversion_funcs = {"slice_obj": check_and_convert_slice_obj,
                                       "seed": check_and_convert_seed}
    pre_serialization_funcs = {"slice_obj": pre_serialize_slice_obj, 
                               "seed": pre_serialize_seed}
    de_pre_serialization_funcs = {"slice_obj": de_pre_serialize_slice_obj, 
                                  "seed": de_pre_serialize_seed}
    params_to_be_mapped_to_core_attrs = {"slice_obj": slice_obj_1,
                                         "seed": 5.0}

    ctor_params = {"validation_and_conversion_funcs": \
                   validation_and_conversion_funcs,
                   "pre_serialization_funcs": \
                   pre_serialization_funcs,
                   "de_pre_serialization_funcs": \
                   de_pre_serialization_funcs,
                   "params_to_be_mapped_to_core_attrs": \
                   params_to_be_mapped_to_core_attrs,
                   "skip_validation_and_conversion": \
                   False}
    kwargs = ctor_params
    fancytype_instance = fancytypes.PreSerializableAndUpdatable(**kwargs)

    new_core_attr_subset_candidate = {"slice_obj": slice_obj_2,
                                      "not_a_core_attr": None}
    kwargs = {"new_core_attr_subset_candidate": new_core_attr_subset_candidate,
              "skip_validation_and_conversion": False}
    fancytype_instance.update(**kwargs)
        
    core_attrs = fancytype_instance.get_core_attrs(deep_copy=False)
    assert core_attrs["slice_obj"] == slice_obj_2
    assert core_attrs["slice_obj"] is not slice_obj_2

    new_core_attr_subset_candidate = {"slice_obj": slice_obj_1}
    kwargs = {"new_core_attr_subset_candidate": new_core_attr_subset_candidate,
              "skip_validation_and_conversion": True}
    fancytype_instance.update(**kwargs)

    core_attrs = fancytype_instance.get_core_attrs(deep_copy=False)
    assert core_attrs["slice_obj"] is slice_obj_1

    core_attrs = fancytype_instance.get_core_attrs(deep_copy=True)
    assert core_attrs["slice_obj"] is not slice_obj_1

    return None



def test_2_of_PreSerializableAndUpdatable():
    slice_obj = slice(None, 6, 1)

    validation_and_conversion_funcs = {"slice_obj": check_and_convert_slice_obj,
                                       "seed": check_and_convert_seed}
    pre_serialization_funcs = {"slice_obj": pre_serialize_slice_obj, 
                               "seed": pre_serialize_seed}
    de_pre_serialization_funcs = {"slice_obj": de_pre_serialize_slice_obj, 
                                  "seed": de_pre_serialize_seed}
    params_to_be_mapped_to_core_attrs = {"slice_obj": slice_obj,
                                         "seed": 5.0}

    ctor_params = {"validation_and_conversion_funcs": \
                   validation_and_conversion_funcs,
                   "pre_serialization_funcs": \
                   pre_serialization_funcs,
                   "de_pre_serialization_funcs": \
                   de_pre_serialization_funcs,
                   "params_to_be_mapped_to_core_attrs": \
                   params_to_be_mapped_to_core_attrs,
                   "skip_validation_and_conversion": \
                   True}
    kwargs = ctor_params
    fancytype_instance = fancytypes.PreSerializableAndUpdatable(**kwargs)

    core_attrs = fancytype_instance.get_core_attrs(deep_copy=False)
    assert core_attrs["slice_obj"] is slice_obj

    fancytype_instance.validation_and_conversion_funcs
    fancytype_instance.pre_serialization_funcs
    fancytype_instance.de_pre_serialization_funcs

    serializable_rep = fancytype_instance.pre_serialize()
    serialized_rep = fancytype_instance.dumps()
    
    filename = "slice_shuffler.json"    
    fancytype_instance.dump(filename, overwrite=True)
    fancytype_instance.dump(filename, overwrite=True)
    with pytest.raises(IOError) as err_info:
        fancytype_instance.dump(filename, overwrite=False)

    pathlib.Path(filename).unlink()

    return None



def test_3_of_PreSerializableAndUpdatable():
    validation_and_conversion_funcs = {"slice_obj": check_and_convert_slice_obj,
                                       "seed": check_and_convert_seed}
    pre_serialization_funcs = {"slice_obj": pre_serialize_slice_obj, 
                               "seed": pre_serialize_seed}
    de_pre_serialization_funcs = {"slice_obj": de_pre_serialize_slice_obj, 
                                  "seed": de_pre_serialize_seed}
    params_to_be_mapped_to_core_attrs = {"slice_obj": slice(None, 6, 1),
                                         "seed": 5.0}

    ctor_params = {"validation_and_conversion_funcs": \
                   validation_and_conversion_funcs,
                   "pre_serialization_funcs": \
                   pre_serialization_funcs,
                   "de_pre_serialization_funcs": \
                   de_pre_serialization_funcs,
                   "params_to_be_mapped_to_core_attrs": \
                   params_to_be_mapped_to_core_attrs,
                   "skip_validation_and_conversion": \
                   True}
    kwargs = ctor_params
    cls_alias = fancytypes.PreSerializableAndUpdatable
    fancytype_instance_A = cls_alias(**kwargs)
    fancytype_instances = (fancytype_instance_A,)

    serializable_rep = fancytype_instance_A.pre_serialize()
    serialized_rep = fancytype_instance_A.dumps()
    filename = "slice_shuffler.json"    
    fancytype_instance_A.dump(filename, overwrite=True)
    
    fancytype_instances += (cls_alias.loads(serialized_rep),
                            cls_alias.load(filename),
                            cls_alias.de_pre_serialize(serializable_rep))

    for fancytype_instance_B in fancytype_instances:
        assert (fancytype_instance_A.core_attrs
                == fancytype_instance_B.core_attrs)

    pathlib.Path(filename).unlink()

    return None



###########################
## Define error messages ##
###########################
