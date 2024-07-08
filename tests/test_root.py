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



# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



##################################
## Define classes and functions ##
##################################



def _check_and_convert_slice_obj(params):
    slice_obj = copy.deepcopy(params["slice_obj"])
    if not isinstance(slice_obj, slice):
        err_msg = ("The object ``slice_obj`` must be of type `slice`.")
        raise TypeError(err_msg)

    return slice_obj



def _check_and_convert_seed(params):
    seed = params["seed"]
    
    if seed is not None:
        try:
            seed = float(seed)
            if seed.is_integer():
                seed = int(seed)
            else:
                raise TypeError
        except:
            err_msg = ("The object ``seed`` must be an integer or `NoneType`.")
            raise TypeError(err_msg)
            
    return seed



def _pre_serialize_slice_obj(slice_obj):
    serializable_rep = {"start": slice_obj.start, 
                        "stop": slice_obj.stop, 
                        "step": slice_obj.step}
    
    return serializable_rep



def _pre_serialize_seed(seed):
    serializable_rep = seed
    
    return serializable_rep




def _de_pre_serialize_slice_obj(serializable_rep):
    slice_obj = slice(serializable_rep["start"], 
                      serializable_rep["stop"], 
                      serializable_rep["step"])
    
    return slice_obj



def _de_pre_serialize_seed(serializable_rep):
    seed = serializable_rep
    
    return seed



class SliceShufflerVersion1(fancytypes.PreSerializableAndUpdatable):
    _validation_and_conversion_funcs = \
        {"slice_obj": _check_and_convert_slice_obj, 
         "seed": _check_and_convert_seed}
    
    _pre_serialization_funcs = \
        {"slice_obj": _pre_serialize_slice_obj, 
         "seed": _pre_serialize_seed}
    
    _de_pre_serialization_funcs = \
        {"slice_obj": _de_pre_serialize_slice_obj, 
         "seed": _de_pre_serialize_seed}
    
    def __init__(self, slice_obj, seed):
        ctor_params = {"slice_obj": slice_obj, "seed": seed}
        fancytypes.PreSerializableAndUpdatable.__init__(self, ctor_params)

        return None



    def _post_base_update(self):
        core_attrs = self.get_core_attrs(deep_copy=False)
        seed = core_attrs["seed"]
        self._random_generator = np.random.default_rng(seed)

        return None



    def update(self, core_attr_subset, skip_validation_and_conversion):
        super().update(core_attr_subset, skip_validation_and_conversion)
        self._post_base_update()

        return None



    def shuffle(self, array):
        array = np.array(array)
            
        slice_obj = self.core_attrs["slice_obj"]
        array_slice = array[slice_obj]
        self._random_generator.shuffle(array_slice)
        array[slice_obj] = array_slice

        return array



def test_1_of_PreSerializableAndUpdatable():
    slice_obj_1 = slice(None, 6, 1)
    slice_obj_2 = slice(3, None, 1)
    
    seed_1 = 5.0
    seed_2 = 1.0

    kwargs = ("slice_obj": slice_obj_1, "seed": seed_1}
    slice_shuffler = SliceShufflerVersion1(**kwargs)

    array_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    shuffled_array_1 = slice_shuffler.shuffle(array_1)

    core_attr_subset = {"slice_obj": slice_obj_2, "not_a_core_attr": None}
    slice_shuffler.update(core_attr_subset,
                          skip_validation_and_conversion=False)
    
    core_attrs = slice_shuffler.get_core_attrs(deep_copy=False)
    assert core_attrs["slice_obj"] == slice_obj_2
    assert core_attrs["slice_obj"] is not slice_obj_2

    core_attr_subset = {"slice_obj": slice_obj_1}
    slice_shuffler.update(core_attr_subset,
                          skip_validation_and_conversion=True)

    core_attrs = slice_shuffler.get_core_attrs(deep_copy=False)
    assert core_attrs["slice_obj"] is slice_obj_1

    core_attrs = slice_shuffler.get_core_attrs(deep_copy=True)
    assert core_attrs["slice_obj"] is not slice_obj_1


    func_to_test = czekitout.check.if_instance_of_any_accepted_types

    unformatted_err_msgs = \
        (czekitout.check._check_accepted_types_err_msg_1,
         czekitout.check._check_accepted_types_err_msg_1,
         czekitout.check._if_instance_of_any_accepted_types_err_msg_1,
         czekitout.check._if_instance_of_any_accepted_types_err_msg_2,
         czekitout.check._if_instance_of_any_accepted_types_err_msg_2)

    objs = 2*([1, 2], np.random.default_rng(), tuple, 3)
    
    accepted_type_sets = ((list,),
                          (np.random._generator.Generator,),
                          (type, int),
                          (3, None),
                          tuple(),
                          (np.random.RandomState,),
                          [int, float],
                          (str, list, type))

    obj_names = tuple("obj_"+str(idx+1) for idx in range(len(objs)))

    format_arg_sets = \
        (("accepted_types", "type"),
         ("accepted_types", "type"),
         (obj_names[5], "numpy.random.mtrand.RandomState"),
         (obj_names[6], str(("int", "float")).replace("\'", "`")),
         (obj_names[7], str(("str", "list", "type")).replace("\'", "`")))

    for obj_idx, _ in enumerate(objs):
        kwargs = {"obj": objs[obj_idx],
                  "obj_name": obj_names[obj_idx],
                  "accepted_types": accepted_type_sets[obj_idx]}
        if obj_idx <= 2:
            assert func_to_test(**kwargs) == None
        else:
            args = format_arg_sets[obj_idx-3]
            err_msg = unformatted_err_msgs[obj_idx-3].format(*args)
            with pytest.raises(TypeError) as err_info:
                func_to_test(**kwargs)
            assert str(err_info.value) == err_msg
            
    return None



def test_1_of_if_one_of_any_accepted_strings():
    func_to_test = czekitout.check.if_one_of_any_accepted_strings

    unformatted_err_msgs = \
        (czekitout.check._if_str_like_err_msg_1,
         czekitout.check._if_str_like_seq_err_msg_1,
         czekitout.check._if_one_of_any_accepted_strings_err_msg_1,
         czekitout.check._if_one_of_any_accepted_strings_err_msg_2,
         czekitout.check._if_one_of_any_accepted_strings_err_msg_3)

    std_str_1 = "foo"
    std_str_2 = "bar"
    std_str_3 = "foobar"

    byte_str_1 = bytes(std_str_1, "utf-8")
    numpy_byte_str_1 = np.array(byte_str_1)

    objs = (std_str_1, byte_str_1, 3, std_str_1) + 3*(std_str_3,)
    
    accepted_string_sets = ((byte_str_1, std_str_2),
                            (numpy_byte_str_1, std_str_2),
                            (std_str_1, std_str_2),
                            (3, std_str_2),
                            tuple(),
                            (std_str_1,),
                            (std_str_1, std_str_2))

    obj_names = tuple("obj_"+str(idx+1) for idx in range(len(objs)))

    format_arg_sets = ((obj_names[2],),
                       ("accepted_strings",),
                       ("accepted_strings",),
                       (obj_names[5], std_str_1),
                       (obj_names[6], str((std_str_1, std_str_2))))

    for obj_idx, _ in enumerate(objs):
        kwargs = {"obj": objs[obj_idx],
                  "obj_name": obj_names[obj_idx],
                  "accepted_strings": accepted_string_sets[obj_idx]}
        if obj_idx <= 1:
            assert func_to_test(**kwargs) == None
        else:
            args = format_arg_sets[obj_idx-2]
            err_msg = unformatted_err_msgs[obj_idx-2].format(*args)
            with pytest.raises(TypeError) as err_info:
                func_to_test(**kwargs)
            assert str(err_info.value) == err_msg
            
    return None



def test_1_of_if_complex_numpy_array():
    func_to_test = czekitout.check.if_complex_numpy_array

    obj_name = "obj"

    complex_two_column_numpy_matrix = (np.random.rand(5, 2)
                                       + 1j*np.random.rand(5, 2))
    real_two_column_numpy_matrix = complex_two_column_numpy_matrix.real
    pairs_of_complex_numbers = complex_two_column_numpy_matrix.tolist()
    pairs_of_real_numbers = real_two_column_numpy_matrix.tolist()

    kwargs = {"obj": complex_two_column_numpy_matrix, "obj_name": obj_name}
    expected_result = None
    assert func_to_test(**kwargs) == expected_result

    kwargs = {"obj": real_two_column_numpy_matrix, "obj_name": obj_name}
    expected_exception = TypeError
    with pytest.raises(expected_exception) as err_info:
        func_to_test(**kwargs)

    kwargs = {"obj": pairs_of_complex_numbers, "obj_name": obj_name}
    expected_exception = TypeError
    with pytest.raises(expected_exception) as err_info:
        func_to_test(**kwargs)

    kwargs = {"obj": pairs_of_real_numbers, "obj_name": obj_name}
    expected_exception = TypeError
    with pytest.raises(expected_exception) as err_info:
        func_to_test(**kwargs)

    return None



def test_1_of_if_callable():
    func_to_test = czekitout.check.if_callable

    unformatted_err_msg_1 = czekitout.check._check_obj_name_err_msg_1
    unformatted_err_msg_2 = czekitout.check._if_callable_err_msg_1

    obj_name = "obj"

    err_msg_1 = unformatted_err_msg_1.format("obj_name", "str")
    err_msg_2 = unformatted_err_msg_2.format(obj_name)

    kwargs = {"obj": max, "obj_name": obj_name}
    expected_result = None
    assert func_to_test(**kwargs) == expected_result

    kwargs = {"obj": "_".join, "obj_name": obj_name}
    expected_result = None
    assert func_to_test(**kwargs) == expected_result

    kwargs = {"obj": max, "obj_name": None}
    expected_exception = TypeError
    expected_err_msg = err_msg_1
    with pytest.raises(expected_exception) as err_info:
        func_to_test(**kwargs)
    assert str(err_info.value) == expected_err_msg

    kwargs = {"obj": 3, "obj_name": obj_name}
    expected_exception = TypeError
    expected_err_msg = err_msg_2
    with pytest.raises(expected_exception) as err_info:
        func_to_test(**kwargs)
    assert str(err_info.value) == expected_err_msg

    return None



###########################
## Define error messages ##
###########################
