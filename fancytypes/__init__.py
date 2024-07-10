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
"""``fancytypes`` is a simple Python library that defines some classes with
useful features, such as enforced validation, updatability, pre-serialization,
and de-pre-serialization. These classes can be used to define more complicated
classes that inherit some subset of the aforementioned features.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For performing deep copies.
import copy

# For serializing and deserializing JSON objects.
import json

# For performing operations on file and directory paths.
import pathlib



# For validating and converting objects.
import czekitout.check
import czekitout.convert



# Get version of current package.
from fancytypes.version import __version__



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["Checkable",
           "Updatable",
           "PreSerializable",
           "PreSerializableAndUpdatable"]



def _check_and_convert_validation_and_conversion_funcs(params):
    err_msg_1 = _check_and_convert_validation_and_conversion_funcs_err_msg_1

    obj_name = "validation_and_conversion_funcs"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    validation_and_conversion_funcs = czekitout.convert.to_dict(**kwargs).copy()

    for key in validation_and_conversion_funcs:
        validation_and_conversion_func = validation_and_conversion_funcs[key]
        if not callable(validation_and_conversion_func):
            raise TypeError(err_msg_1)

    return validation_and_conversion_funcs



def _check_and_convert_skip_validation_and_conversion(params):
    obj_name = "skip_validation_and_conversion"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    skip_validation_and_conversion = czekitout.convert.to_bool(**kwargs)

    return skip_validation_and_conversion



def _check_and_convert_params_to_be_mapped_to_core_attrs(params):
    params["core_attrs_candidate"] = \
        params["params_to_be_mapped_to_core_attrs"]
    params["name_of_obj_alias_of_core_attrs_candidate"] = \
        "params_to_be_mapped_to_core_attrs"
    params_to_be_mapped_to_core_attrs = \
        _check_and_convert_core_attrs_candidate(params)

    del params["core_attrs_candidate"]
    del params["name_of_obj_alias_of_core_attrs_candidate"]

    return params_to_be_mapped_to_core_attrs



def _check_and_convert_core_attrs_candidate(params):
    unformatted_err_msg_1 = _check_and_convert_core_attrs_candidate_err_msg_1

    obj_name = \
        params["name_of_obj_alias_of_core_attrs_candidate"]
    kwargs = \
        {"obj": params["core_attrs_candidate"], "obj_name": obj_name}
    core_attrs_candidate = \
        czekitout.convert.to_dict(**kwargs).copy()

    validation_and_conversion_funcs = \
        params["validation_and_conversion_funcs"]

    key_set_1 = sorted(list(validation_and_conversion_funcs.keys()))
    key_set_2 = sorted(list(core_attrs_candidate.keys()))
    if key_set_1 != key_set_2:
        obj_name = params["name_of_obj_alias_of_core_attrs_candidate"]
        err_msg_1 = unformatted_err_msg_1.format(obj_name)
        raise KeyError(err_msg_1)
        
    for key in validation_and_conversion_funcs:
        validation_and_conversion_func = validation_and_conversion_funcs[key]
        
        kwargs = \
            {"params": core_attrs_candidate}
        core_attr_candidate = \
            validation_and_conversion_func(**kwargs)
        
        core_attrs_candidate[key] = \
            core_attr_candidate

    return core_attrs_candidate



_default_skip_validation_and_conversion = False



class Checkable():
    r"""A type that can perform user-defined validations and conversions of a 
    set of parameters upon construction.

    Parameters
    ----------
    validation_and_conversion_funcs : `dict`
        A `dict` object of callable objects.
    params_to_be_mapped_to_core_attrs : `dict`
        A `dict` object that has the same keys as
        ``validation_and_conversion_funcs``.
    skip_validation_and_conversion : `bool`
        Let ``core_attrs`` denote the attribute
        :attr:`fancytypes.Checkable.core_attrs`, which is a `dict` object.

        If ``skip_validation_and_conversion`` is set to ``False``, then for each
        key ``key`` in ``validation_and_conversion_funcs``, ``core_attrs[key]``
        is set to ``validation_and_conversion_funcs[key]
        (params_to_be_mapped_to_core_attrs)``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then ``core_attrs`` is set to
        ``params_to_be_mapped_to_core_attrs``. This option is desired primarily
        when the user wants to avoid potentially expensive copies and/or
        conversions of the `dict` values of
        ``params_to_be_mapped_to_core_attrs``, as it is guaranteed that no
        copies or conversions are made in this case.
    
    Attributes
    ----------
    validation_and_conversion_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    core_attrs : `dict`, read-only
        The "core attributes", represented as a `dict` object. For each `dict`
        key ``key`` in ``core_attrs``,
        ``validation_and_conversion_funcs[key](core_attrs)`` is expected to not
        raise an exception.

    """
    def __init__(self,
                 validation_and_conversion_funcs,
                 params_to_be_mapped_to_core_attrs,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        ctor_params = {key: val
                       for key, val in locals().items()
                       if (key not in ("self", "__class__"))}

        func_alias = _check_and_convert_validation_and_conversion_funcs
        self._validation_and_conversion_funcs = func_alias(params=ctor_params)

        params = \
            {"skip_validation_and_conversion": skip_validation_and_conversion}
        skip_validation_and_conversion = \
            _check_and_convert_skip_validation_and_conversion(params)

        if (skip_validation_and_conversion == False):
            params = \
                ctor_params
            self._core_attrs = \
                _check_and_convert_params_to_be_mapped_to_core_attrs(params)
        else:
            self._core_attrs = \
                params_to_be_mapped_to_core_attrs

        return None



    @property
    def core_attrs(self):
        result = copy.deepcopy(self._core_attrs)
        
        return result



    @property
    def validation_and_conversion_funcs(self):
        result = copy.deepcopy(self._validation_and_conversion_funcs)
        
        return result


def _update_old_core_attr_set_and_return_new_core_attr_set(
        skip_validation_and_conversion,
        new_core_attr_subset_candidate,
        old_core_attr_set,
        validation_and_conversion_funcs):
    params = \
        {"skip_validation_and_conversion": skip_validation_and_conversion}
    skip_validation_and_conversion = \
        _check_and_convert_skip_validation_and_conversion(params)

    kwargs = {"obj": new_core_attr_subset_candidate,
              "obj_name": "new_core_attr_subset_candidate"}
    czekitout.check.if_dict_like(**kwargs)
    
    new_core_attr_set = new_core_attr_subset_candidate.copy()

    for core_attr_name in old_core_attr_set.keys():
        if core_attr_name not in new_core_attr_subset_candidate:
            new_core_attr_candidate = old_core_attr_set[core_attr_name]
            new_core_attr_set[core_attr_name] = new_core_attr_candidate

    names_of_core_attrs_to_update = tuple()
    for core_attr_name in new_core_attr_subset_candidate:
        if core_attr_name not in old_core_attr_set:
            del new_core_attr_set[core_attr_name]
        else:
            names_of_core_attrs_to_update += (core_attr_name,)

    for ctor_param_name in names_of_core_attrs_to_update:
        validation_and_conversion_func = \
            validation_and_conversion_funcs[ctor_param_name]

        if (skip_validation_and_conversion == False):
            new_core_attr = validation_and_conversion_func(new_core_attr_set)
            new_core_attr_set[ctor_param_name] = new_core_attr

    return new_core_attr_set



def _check_and_convert_deep_copy(params):
    obj_name = "deep_copy"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    deep_copy = czekitout.convert.to_bool(**kwargs)

    return deep_copy



_default_deep_copy = True



class Updatable(Checkable):
    r"""A type that can perform user-defined validations and conversions of a 
    set of parameters upon construction, and that has an updatable subset of 
    attributes.

    Parameters
    ----------
    validation_and_conversion_funcs : `dict`
        A `dict` object of callable objects.
    params_to_be_mapped_to_core_attrs : `dict`
        A `dict` object that has the same keys as
        ``validation_and_conversion_funcs``.
    skip_validation_and_conversion : `bool`
        Let ``core_attrs`` denote the attribute
        :attr:`fancytypes.Updatable.core_attrs`, which is a `dict` object.

        If ``skip_validation_and_conversion`` is set to ``False``, then for each
        key ``key`` in ``validation_and_conversion_funcs``, ``core_attrs[key]``
        is set to ``validation_and_conversion_funcs[key]
        (params_to_be_mapped_to_core_attrs)``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then ``core_attrs`` is set to
        ``params_to_be_mapped_to_core_attrs``. This option is desired primarily
        when the user wants to avoid potentially expensive copies and/or
        conversions of the `dict` values of
        ``params_to_be_mapped_to_core_attrs``, as it is guaranteed that no
        copies or conversions are made in this case.

    Attributes
    ----------
    validation_and_conversion_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    core_attrs : `dict`, read-only
        The "core attributes", represented as a `dict` object. For each `dict`
        key ``key`` in ``core_attrs``,
        ``validation_and_conversion_funcs[key](core_attrs)`` is expected to not
        raise an exception.

    """
    def __init__(self,
                 validation_and_conversion_funcs,
                 params_to_be_mapped_to_core_attrs,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        ctor_params = {key: val
                       for key, val in locals().items()
                       if (key not in ("self", "__class__"))}
        kwargs = ctor_params
        Checkable.__init__(self, **kwargs)

        return None



    def update(self,
               new_core_attr_subset_candidate,
               skip_validation_and_conversion=\
               _default_skip_validation_and_conversion):
        r"""Update a subset of the core attributes.

        Parameters
        ----------
        new_core_attr_subset_candidate : `dict`
            A `dict` object.
        skip_validation_and_conversion : `bool`
            Let ``core_attrs`` and ``validation_and_conversion_funcs`` denote
            the attributes :attr:`fancytypes.Updatable.core_attrs` and
            :attr:`fancytypes.Updatable.validation_and_conversion_funcs`
            respectively, which are both `dict` objects.

            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``core_attrs`` that is also in
            ``new_core_attr_subset_candidate``, ``core_attrs[key]`` is set to
            ``validation_and_conversion_funcs[key]
            (new_core_attr_subset_candidate)``.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then for each key ``key`` in ``core_attrs`` that is also in
            ``new_core_attr_subset_candidate``, ``core_attrs[key]`` is set to
            ``new_core_attr_subset_candidate[key]``. This option is desired
            primarily when the user wants to avoid potentially expensive copies
            and/or conversions of the `dict` values of
            ``new_core_attr_subset_candidate``, as it is guaranteed that no
            copies or conversions are made in this case.

        """
        kwargs = \
            {"skip_validation_and_conversion": \
             skip_validation_and_conversion,
             "new_core_attr_subset_candidate": \
             new_core_attr_subset_candidate,
             "old_core_attr_set": \
             self._core_attrs,
             "validation_and_conversion_funcs": \
             self._validation_and_conversion_funcs}
        self._core_attrs = \
            _update_old_core_attr_set_and_return_new_core_attr_set(**kwargs)

        return None



    def get_core_attrs(self, deep_copy=_default_deep_copy):
        r"""Return the core attributes.

        Parameters
        ----------
        deep_copy : `bool`
            If ``deep_copy`` is set to ``True``, then a deep copy of the 
            original `dict` representation of the core attributes are returned. 
            Otherwise, a reference to the `dict` representation is returned.

        Returns
        -------
        core_attrs : `dict`
            A `dict` representation of the core attributes: each `dict` key is a
            `str` representing the name of a core attribute, and the 
            corresponding `dict` value is the object to which said core 
            attribute is set.

        """
        params = {"deep_copy": deep_copy}
        deep_copy = _check_and_convert_deep_copy(params)
        
        core_attrs = (self.core_attrs
                      if (deep_copy == True)
                      else self._core_attrs)

        return core_attrs



def _preliminary_check_of_pre_serialization_funcs(params):
    err_msg_1 = _preliminary_check_of_pre_serialization_funcs_err_msg_1
    err_msg_2 = _preliminary_check_of_pre_serialization_funcs_err_msg_2

    obj_name = "pre_serialization_funcs"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    pre_serialization_funcs = czekitout.convert.to_dict(**kwargs)

    validation_and_conversion_funcs = params["validation_and_conversion_funcs"]

    key_set_1 = sorted(list(validation_and_conversion_funcs.keys()))
    key_set_2 = sorted(list(pre_serialization_funcs.keys()))
    if key_set_1 != key_set_2:
        raise KeyError(err_msg_1)
    
    for key in pre_serialization_funcs:
        pre_serialization_func = pre_serialization_funcs[key]
        if not callable(pre_serialization_func):
            raise TypeError(err_msg_2)

    return None



def _preliminary_check_of_de_pre_serialization_funcs(params):
    err_msg_1 = _preliminary_check_of_de_pre_serialization_funcs_err_msg_1
    err_msg_2 = _preliminary_check_of_de_pre_serialization_funcs_err_msg_2

    obj_name = "de_pre_serialization_funcs"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    de_pre_serialization_funcs = czekitout.convert.to_dict(**kwargs)

    validation_and_conversion_funcs = params["validation_and_conversion_funcs"]

    key_set_1 = sorted(list(validation_and_conversion_funcs.keys()))
    key_set_2 = sorted(list(de_pre_serialization_funcs.keys()))
    if key_set_1 != key_set_2:
        raise KeyError(err_msg_1)
    
    for key in de_pre_serialization_funcs:
        de_pre_serialization_func = de_pre_serialization_funcs[key]
        if not callable(de_pre_serialization_func):
            raise TypeError(err_msg_2)

    return None



def _check_and_convert_overwrite(params):
    obj_name = "overwrite"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    overwrite = czekitout.convert.to_bool(**kwargs)

    return overwrite



_default_overwrite = False



class PreSerializable(Checkable):
    r"""A type that is pre-serializable, that can be constructed from a 
    serializable representation, and that can perform user-defined validations 
    and conversions of a set of parameters upon construction.

    We define pre-serialization as the process of converting an object into a
    form that can be subsequently serialized into a JSON format. We refer to
    objects resulting from pre-serialization as serializable objects.

    We define de-pre-serialization as the process of converting a serializable
    object into an instance of the type :class:`fancytypes.PreSerializable` or a
    subclass thereof, i.e. de-pre-serialization is the reverse process of
    pre-serialization.

    Parameters
    ----------
    validation_and_conversion_funcs : `dict`
        A `dict` object of callable objects.
    pre_serialization_funcs : `dict`
        A `dict` object of callable objects that has the same keys as
        ``validation_and_conversion_funcs``. 

        Let ``core_attrs_candidate_1`` be any `dict` object that has the same
        keys as ``validation_and_conversion_funcs`` where for each `dict` key
        ``key`` in ``validation_and_conversion_funcs``,
        ``validation_and_conversion_funcs[key](core_attrs_candidate_1)`` does
        not raise an exception.

        For each `dict` key ``key`` in ``validation_and_conversion_funcs``,
        ``pre_serialization_funcs[key](core_attrs_candidate_1[key])`` is
        expected to yield a serializable object, i.e. it should yield an object
        that can be passed into the function ``json.dumps`` without raising an
        exception.
    de_pre_serialization_funcs : `dict`
        A `dict` object of callable objects that has the same keys as
        ``validation_and_conversion_funcs``. 

        Let ``serializable_rep`` be a `dict` object that has the same keys as
        ``validation_and_conversion_funcs`` where for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``, ``serializable_rep[key]`` is set to
        ``pre_serialization_funcs[key](core_attrs_candidate_1[key])``, with
        ``core_attrs_candidate_1`` being defined in the above description of
        ``pre_serialization_funcs``.

        The items of ``de_pre_serialization_funcs`` are expected to be set to
        callable objects that would lead to
        ``de_pre_serialization_funcs[key](serializable_rep[key])`` not raising
        an exception for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``.

        Let ``core_attrs_candidate_2`` be a `dict` object that has the same keys
        as ``validation_and_conversion_funcs`` where for each `dict` key ``key``
        in ``validation_and_conversion_funcs``, ``core_attrs_candidate_2[key]``
        is set to ``de_pre_serialization_funcs[key](serializable_rep[key])``.

        The items of ``de_pre_serialization_funcs`` are also expected to be set
        to callable objects that would lead to
        ``validation_and_conversion_funcs[key](core_attrs_candidate_2)`` not
        raising an exception for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``.
    params_to_be_mapped_to_core_attrs : `dict`
        A `dict` object that has the same keys as
        ``validation_and_conversion_funcs``.
    skip_validation_and_conversion : `bool`
        Let ``core_attrs`` denote the attribute
        :attr:`fancytypes.PreSerializable.core_attrs`, which is a `dict` object.

        If ``skip_validation_and_conversion`` is set to ``False``, then for each
        key ``key`` in ``validation_and_conversion_funcs``, ``core_attrs[key]``
        is set to ``validation_and_conversion_funcs[key]
        (params_to_be_mapped_to_core_attrs)``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then ``core_attrs`` is set to
        ``params_to_be_mapped_to_core_attrs``. This option is desired primarily
        when the user wants to avoid potentially expensive copies and/or
        conversions of the `dict` values of
        ``params_to_be_mapped_to_core_attrs``, as it is guaranteed that no
        copies or conversions are made in this case.

    Attributes
    ----------
    validation_and_conversion_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    pre_serialization_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    de_pre_serialization_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    core_attrs : `dict`, read-only
        The "core attributes", represented as a `dict` object. For each `dict`
        key ``key`` in ``core_attrs``,
        ``validation_and_conversion_funcs[key](core_attrs)`` is expected to not
        raise an exception.

    """
    def __init__(self,
                 validation_and_conversion_funcs,
                 pre_serialization_funcs,
                 de_pre_serialization_funcs,
                 params_to_be_mapped_to_core_attrs,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        ctor_params = {key: val
                       for key, val in locals().items()
                       if (key not in ("self", "__class__"))}
        
        kwargs = {"validation_and_conversion_funcs": \
                  validation_and_conversion_funcs,
                  "params_to_be_mapped_to_core_attrs": \
                  params_to_be_mapped_to_core_attrs,
                  "skip_validation_and_conversion": \
                  skip_validation_and_conversion}
        Checkable.__init__(self, **kwargs)

        _preliminary_check_of_pre_serialization_funcs(params=ctor_params)
        self._pre_serialization_funcs = dict(pre_serialization_funcs)

        _preliminary_check_of_de_pre_serialization_funcs(params=ctor_params)
        self._de_pre_serialization_funcs = dict(de_pre_serialization_funcs)
        
        if (skip_validation_and_conversion == False):
            try:
                serializable_rep = self.pre_serialize()
            except:
                raise ValueError(_pre_serializable_err_msg_1)
        
            try:
                kwargs = \
                    {"serializable_rep": serializable_rep,
                     "de_pre_serialization_funcs": de_pre_serialization_funcs}
                core_attrs_candidate = \
                    self._construct_core_attrs_candidate(**kwargs)

                params = {"core_attrs_candidate": \
                          core_attrs_candidate,
                          "name_of_obj_alias_of_core_attrs_candidate": \
                          "core_attrs_candidate",
                          "validation_and_conversion_funcs": \
                          validation_and_conversion_funcs}
                _ =_check_and_convert_core_attrs_candidate(params)
            except:
                raise ValueError(_pre_serializable_err_msg_2)
        
        return None



    @classmethod
    def _construct_core_attrs_candidate(cls,
                                        serializable_rep,
                                        de_pre_serialization_funcs):
        kwargs = {"obj": serializable_rep, "obj_name": "serializable_rep"}
        serializable_rep = czekitout.convert.to_dict(**kwargs)

        for key in de_pre_serialization_funcs:
            if key not in serializable_rep:
                err_msg = _pre_serializable_err_msg_3.format(key)
                raise KeyError(err_msg)
            
        try:
            core_attrs_candidate = dict()
            
            for key in de_pre_serialization_funcs:
                core_attr_name = \
                    key
                elem_of_serializable_rep = \
                    serializable_rep[key]
                de_pre_serialization_func = \
                    de_pre_serialization_funcs[key]
                core_attr_candidate = \
                    de_pre_serialization_func(elem_of_serializable_rep)
                core_attrs_candidate[core_attr_name] = \
                    core_attr_candidate
        except:
            err_msg = _pre_serializable_err_msg_4
            raise ValueError(err_msg)

        return core_attrs_candidate



    @classmethod
    def de_pre_serialize(cls,
                         validation_and_conversion_funcs,
                         pre_serialization_funcs,
                         de_pre_serialization_funcs,
                         serializable_rep,
                         skip_validation_and_conversion=\
                         _default_skip_validation_and_conversion):
        r"""Construct an instance from a serializable representation.

        We define pre-serialization as the process of converting an object into
        a form that can be subsequently serialized into a JSON format. We refer
        to objects resulting from pre-serialization as serializable objects.

        We define de-pre-serialization as the process of converting a
        serializable object into an instance of the type
        :class:`fancytypes.PreSerializable` or a subclass thereof,
        i.e. de-pre-serialization is the reverse process of pre-serialization.

        Parameters
        ----------
        validation_and_conversion_funcs : `dict`
            Same as the constructor parameter of the same name.
        pre_serialization_funcs : `dict`
            Same as the constructor parameter of the same name.
        de_pre_serialization_funcs : `dict`
            Same as the constructor parameter of the same name.
        serializable_rep : `dict`
            A `dict` object that has the same keys as
            ``validation_and_conversion_funcs``.

            The items of ``serializable_rep`` are expected to be set to callable
            objects that would lead to
            ``de_pre_serialization_funcs[key](serializable_rep[key])`` not
            raising an exception for each `dict` key ``key`` in
            ``validation_and_conversion_funcs``.

            Let ``core_attrs_candidate`` be a `dict` object that has the same
            keys as ``validation_and_conversion_funcs`` where for each `dict`
            key ``key`` in ``validation_and_conversion_funcs``,
            ``core_attrs_candidate[key]`` is set to
            de_pre_serialization_funcs[key](serializable_rep[key])``.

            The items of ``serializable_rep`` are also expected to be set to
            objects that would lead to
            ``validation_and_conversion_funcs[key](core_attrs_candidate)`` not
            raising an exception for each `dict` key ``key`` in
            ``validation_and_conversion_funcs``.
        skip_validation_and_conversion : `bool`
            Let ``core_attrs`` denote the attribute
            :attr:`fancytypes.PreSerializable.core_attrs`, which is a `dict`
            object.

            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``validation_and_conversion_funcs``,
            ``core_attrs[key]`` is set to ``validation_and_conversion_funcs[key]
            (core_attrs_candidate)``, with ``core_attrs_candidate_`` being
            defined in the above description of ``serializable_rep``.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then ``core_attrs`` is set to ``core_attrs_candidate``. This option
            is desired primarily when the user wants to avoid potentially
            expensive copies and/or conversions of the `dict` values of
            ``core_attrs_candidate``, as it is guaranteed that no copies or
            conversions are made in this case.

        Returns
        -------
        pre_serializable_obj : Current class
            An instance constructed from the serializable representation
            ``serializable_rep``.

        """
        params = {key: val
                  for key, val in locals().items()
                  if (key not in ("self", "__class__"))}

        _preliminary_check_of_de_pre_serialization_funcs(params)
        de_pre_serialization_funcs = dict(de_pre_serialization_funcs)

        try:
            kwargs = \
                {"serializable_rep": serializable_rep,
                 "de_pre_serialization_funcs": de_pre_serialization_funcs}
            core_attrs_candidate = \
                cls._construct_core_attrs_candidate(**kwargs)

            kwargs = {"validation_and_conversion_funcs": \
                      validation_and_conversion_funcs,
                      "pre_serialization_funcs": \
                      pre_serialization_funcs,
                      "de_pre_serialization_funcs": \
                      de_pre_serialization_funcs,
                      "params_to_be_mapped_to_core_attrs": \
                      core_attrs_candidate,
                      "skip_validation_and_conversion": \
                      True}
            pre_serializable_obj = cls(**kwargs)

            if (skip_validation_and_conversion == False):
                try:
                    _ = pre_serializable_obj.pre_serialize()
                except:
                    raise ValueError(_pre_serializable_err_msg_1)

                params = {"core_attrs_candidate": \
                          pre_serializable_obj._core_attrs,
                          "name_of_obj_alias_of_core_attrs_candidate": \
                          "pre_serializable_obj._core_attrs",
                          "validation_and_conversion_funcs": \
                          validation_and_conversion_funcs}
                core_attrs = _check_and_convert_core_attrs_candidate(params)
                pre_serializable_obj._core_attrs = core_attrs
        except:
            raise ValueError(_pre_serializable_err_msg_5)
                
        return pre_serializable_obj



    def pre_serialize(self):
        r"""Pre-serialize instance.

        We define pre-serialization as the process of converting an object into
        a form that can be subsequently serialized into a JSON format. We refer
        to objects resulting from pre-serialization as serializable objects.

        We define de-pre-serialization as the process of converting a
        serializable object into an instance of the type
        :class:`fancytypes.PreSerializable` or a subclass thereof,
        i.e. de-pre-serialization is the reverse process of pre-serialization.

        Returns
        -------
        serializable_rep : `dict`
            A serializable representation of an instance.

        """
        serializable_rep = dict()
        
        for core_attr_name, core_attr in self._core_attrs.items():
            pre_serialization_func = \
                self._pre_serialization_funcs[core_attr_name]
            elem_of_serializable_rep = \
                pre_serialization_func(core_attr)
            serializable_rep[core_attr_name] = \
                elem_of_serializable_rep

        return serializable_rep



    def dumps(self):
        r"""Serialize instance.
        
        Returns
        -------
        serialized_rep : `dict`
            A serialized representation of an instance.

        """
        serializable_rep = self.pre_serialize()
        serialized_rep = json.dumps(serializable_rep)

        return serialized_rep



    def dump(self, filename, overwrite=_default_overwrite):
        r"""Serialize instance and save the result in a JSON file.

        Parameters
        ----------
        filename : `str`
            The relative or absolute path to the JSON file in which to store the
            serialized representation of an instance.
        overwrite : `bool`, optional
            If ``overwrite`` is set to ``False`` and a file exists at the path
            ``filename``, then the serialized instance is not written to that
            file and an exception is raised. Otherwise, the serialized instance
            will be written to that file barring no other issues occur.

        Returns
        -------

        """
        params = {"overwrite": overwrite}
        overwrite = _check_and_convert_overwrite(params)
        
        kwargs = {"obj": filename, "obj_name": "filename"}
        filename = czekitout.convert.to_str_from_str_like(**kwargs)
        if pathlib.Path(filename).is_file():
            if not overwrite:
                raise IOError(_pre_serializable_err_msg_6.format(filename))

        serializable_rep = self.pre_serialize()

        try:
            with open(filename, "w", encoding="utf-8") as file_obj:
                json.dump(serializable_rep,
                          file_obj,
                          ensure_ascii=False,
                          indent=4)
        except:
            raise IOError(_pre_serializable_err_msg_7.format(filename))
            
        return None



    @classmethod
    def loads(cls,
              validation_and_conversion_funcs,
              pre_serialization_funcs,
              de_pre_serialization_funcs,
              serialized_rep,
              skip_validation_and_conversion=\
              _default_skip_validation_and_conversion):
        r"""Construct an instance from a serialized representation.

        Users can generate serialized representations using the method
        :meth:`fancytypes.PreSerializable.dumps`.

        Parameters
        ----------
        validation_and_conversion_funcs : `dict`
            Same as the constructor parameter of the same name.
        pre_serialization_funcs : `dict`
            Same as the constructor parameter of the same name.
        de_pre_serialization_funcs : `dict`
            Same as the constructor parameter of the same name.
        serialized_rep : `str` | `bytes` | `bytearray`
            The serialized representation.

            ``serialized_rep`` is expected to be such that
            ``json.loads(serialized_rep)`` does not raise an exception.

            Let ``serializable_rep=json.loads(serialized_rep)``. 

            ``serialized_rep`` is also expected to be such that
            ``de_pre_serialization_funcs[key](serializable_rep[key])`` does not
            raise an exception for each `dict` key ``key`` in
            ``validation_and_conversion_funcs``.

            Let ``core_attrs_candidate`` be a `dict` object that has the same
            keys as ``validation_and_conversion_funcs`` where for each `dict`
            key ``key`` in ``validation_and_conversion_funcs``,
            ``core_attrs_candidate[key]`` is set to
            de_pre_serialization_funcs[key](serializable_rep[key])``.

            ``serialized_rep`` is also expected to be such that
            ``validation_and_conversion_funcs[key](core_attrs_candidate)`` does
            not raising an exception for each `dict` key ``key`` in
            ``validation_and_conversion_funcs``.
        skip_validation_and_conversion : `bool`
            Let ``core_attrs`` denote the attribute
            :attr:`fancytypes.PreSerializable.core_attrs`, which is a `dict`
            object.

            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``validation_and_conversion_funcs``,
            ``core_attrs[key]`` is set to ``validation_and_conversion_funcs[key]
            (core_attrs_candidate)``, with ``core_attrs_candidate_`` being
            defined in the above description of ``serializable_rep``.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then ``core_attrs`` is set to ``core_attrs_candidate``. This option
            is desired primarily when the user wants to avoid potentially
            expensive copies and/or conversions of the `dict` values of
            ``core_attrs_candidate``, as it is guaranteed that no copies or
            conversions are made in this case.

        Returns
        -------
        pre_serializable_obj : Current class
            An instance constructed from the serialized representation.

        """
        kwargs = {"obj": serialized_rep,
                  "obj_name": "serialized_rep",
                  "accepted_types": (str, bytes, bytearray)}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)
        
        try:
            serializable_rep = json.loads(serialized_rep)
        except:
            raise ValueError(_pre_serializable_err_msg_8)

        kwargs = {"validation_and_conversion_funcs": \
                  validation_and_conversion_funcs,
                  "pre_serialization_funcs": \
                  pre_serialization_funcs,
                  "de_pre_serialization_funcs": \
                  de_pre_serialization_funcs,
                  "serializable_rep": \
                  serializable_rep,
                  "skip_validation_and_conversion": \
                  skip_validation_and_conversion}
        pre_serializable_obj = cls.de_pre_serialize(**kwargs)
                
        return pre_serializable_obj



    @classmethod
    def load(cls,
             validation_and_conversion_funcs,
             pre_serialization_funcs,
             de_pre_serialization_funcs,
             filename,
             skip_validation_and_conversion=\
             _default_skip_validation_and_conversion):
        r"""Construct an instance from a serialized representation that is 
        stored in a JSON file.

        Users can save serialized representations to JSON files using the method
        :meth:`fancytypes.PreSerializable.dump`.

        Parameters
        ----------
        validation_and_conversion_funcs : `dict`
            Same as the constructor parameter of the same name.
        pre_serialization_funcs : `dict`
            Same as the constructor parameter of the same name.
        de_pre_serialization_funcs : `dict`
            Same as the constructor parameter of the same name.
        filename : `str`
            The relative or absolute path to the JSON file that is storing the
            serialized representation of an instance.

            ``filename`` is expected to be such that ``json.load(open(filename,
            "r"))`` does not raise an exception.

            Let ``serializable_rep=json.load(open(filename, "r"))``.

            ``filename`` is also expected to be such that
            ``de_pre_serialization_funcs[key](serializable_rep[key])`` does not
            raise an exception for each `dict` key ``key`` in
            ``validation_and_conversion_funcs``.

            Let ``core_attrs_candidate`` be a `dict` object that has the same
            keys as ``validation_and_conversion_funcs`` where for each `dict`
            key ``key`` in ``validation_and_conversion_funcs``,
            ``core_attrs_candidate[key]`` is set to
            de_pre_serialization_funcs[key](serializable_rep[key])``.

            ``filename`` is also expected to be such that
            ``validation_and_conversion_funcs[key](core_attrs_candidate)`` does
            not raising an exception for each `dict` key ``key`` in
            ``validation_and_conversion_funcs``.
        skip_validation_and_conversion : `bool`
            Let ``core_attrs`` denote the attribute
            :attr:`fancytypes.PreSerializable.core_attrs`, which is a `dict`
            object.

            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``validation_and_conversion_funcs``,
            ``core_attrs[key]`` is set to ``validation_and_conversion_funcs[key]
            (core_attrs_candidate)``, with ``core_attrs_candidate_`` being
            defined in the above description of ``serializable_rep``.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then ``core_attrs`` is set to ``core_attrs_candidate``. This option
            is desired primarily when the user wants to avoid potentially
            expensive copies and/or conversions of the `dict` values of
            ``core_attrs_candidate``, as it is guaranteed that no copies or
            conversions are made in this case.

        Returns
        -------
        pre_serializable_obj : Current class
            An instance constructed from the serialized representation
            stored in the JSON file.

        """
        kwargs = {"obj": filename, "obj_name": "filename"}
        filename = czekitout.convert.to_str_from_str_like(**kwargs)
        
        try:
            with open(filename, "r") as file_obj:
                serializable_rep = json.load(file_obj)
        except:
            raise IOError(_pre_serializable_err_msg_9.format(filename))

        kwargs = {"validation_and_conversion_funcs": \
                  validation_and_conversion_funcs,
                  "pre_serialization_funcs": \
                  pre_serialization_funcs,
                  "de_pre_serialization_funcs": \
                  de_pre_serialization_funcs,
                  "serializable_rep": \
                  serializable_rep,
                  "skip_validation_and_conversion": \
                  skip_validation_and_conversion}
        pre_serializable_obj = cls.de_pre_serialize(**kwargs)
                
        return pre_serializable_obj



    @property
    def pre_serialization_funcs(self):
        result = copy.deepcopy(self._pre_serialization_funcs)
        
        return result



    @property
    def de_pre_serialization_funcs(self):
        result = copy.deepcopy(self._de_pre_serialization_funcs)
        
        return result



class PreSerializableAndUpdatable(PreSerializable):
    r"""A type that is pre-serializable, that can be constructed from a 
    serializable representation, that can perform user-defined validations 
    and conversions of a set of parameters upon construction, and that has an
    updatable subset of attributes.

    We define pre-serialization as the process of converting an object into a
    form that can be subsequently serialized into a JSON format. We refer to
    objects resulting from pre-serialization as serializable objects.

    We define de-pre-serialization as the process of converting a serializable
    object into an instance of the type :class:`fancytypes.PreSerializable` or a
    subclass thereof, i.e. de-pre-serialization is the reverse process of
    pre-serialization.

    Parameters
    ----------
    validation_and_conversion_funcs : `dict`
        A `dict` object of callable objects.
    pre_serialization_funcs : `dict`
        A `dict` object of callable objects that has the same keys as
        ``validation_and_conversion_funcs``. 

        Let ``core_attrs_candidate_1`` be any `dict` object that has the same
        keys as ``validation_and_conversion_funcs`` where for each `dict` key
        ``key`` in ``validation_and_conversion_funcs``,
        ``validation_and_conversion_funcs[key](core_attrs_candidate_1)`` does
        not raise an exception.

        For each `dict` key ``key`` in ``validation_and_conversion_funcs``,
        ``pre_serialization_funcs[key](core_attrs_candidate_1[key])`` is
        expected to yield a serializable object, i.e. it should yield an object
        that can be passed into the function ``json.dumps`` without raising an
        exception.
    de_pre_serialization_funcs : `dict`
        A `dict` object of callable objects that has the same keys as
        ``validation_and_conversion_funcs``. 

        Let ``serializable_rep`` be a `dict` object that has the same keys as
        ``validation_and_conversion_funcs`` where for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``, ``serializable_rep[key]`` is set to
        ``pre_serialization_funcs[key](core_attrs_candidate_1[key])``, with
        ``core_attrs_candidate_1`` being defined in the above description of
        ``pre_serialization_funcs``.

        The items of ``de_pre_serialization_funcs`` are expected to be set to
        callable objects that would lead to
        ``de_pre_serialization_funcs[key](serializable_rep[key])`` not raising
        an exception for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``.

        Let ``core_attrs_candidate_2`` be a `dict` object that has the same keys
        as ``validation_and_conversion_funcs`` where for each `dict` key ``key``
        in ``validation_and_conversion_funcs``, ``core_attrs_candidate_2[key]``
        is set to ``de_pre_serialization_funcs[key](serializable_rep[key])``.

        The items of ``de_pre_serialization_funcs`` are also expected to be set
        to callable objects that would lead to
        ``validation_and_conversion_funcs[key](core_attrs_candidate_2)`` not
        raising an exception for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``.
    params_to_be_mapped_to_core_attrs : `dict`
        A `dict` object that has the same keys as
        ``validation_and_conversion_funcs``.
    skip_validation_and_conversion : `bool`
        Let ``core_attrs`` denote the attribute
        :attr:`fancytypes.PreSerializableAndUpdatable.core_attrs`, which is a 
        `dict` object.

        If ``skip_validation_and_conversion`` is set to ``False``, then for each
        key ``key`` in ``validation_and_conversion_funcs``, ``core_attrs[key]``
        is set to ``validation_and_conversion_funcs[key]
        (params_to_be_mapped_to_core_attrs)``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then ``core_attrs`` is set to
        ``params_to_be_mapped_to_core_attrs``. This option is desired primarily
        when the user wants to avoid potentially expensive copies and/or
        conversions of the `dict` values of
        ``params_to_be_mapped_to_core_attrs``, as it is guaranteed that no
        copies or conversions are made in this case.

    Attributes
    ----------
    validation_and_conversion_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    pre_serialization_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    de_pre_serialization_funcs : `dict`, read-only
        Same as the constructor parameter of the same name.
    core_attrs : `dict`, read-only
        The "core attributes", represented as a `dict` object. For each `dict`
        key ``key`` in ``core_attrs``,
        ``validation_and_conversion_funcs[key](core_attrs)`` is expected to not
        raise an exception.

    """
    def __init__(self,
                 validation_and_conversion_funcs,
                 pre_serialization_funcs,
                 de_pre_serialization_funcs,
                 params_to_be_mapped_to_core_attrs,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        kwargs = {key: val
                  for key, val in locals().items()
                  if (key not in ("self", "__class__"))}
        PreSerializable.__init__(self, **kwargs)
        
        return None



    def update(self,
               new_core_attr_subset_candidate,
               skip_validation_and_conversion=\
               _default_skip_validation_and_conversion):
        r"""Update a subset of the core attributes.

        Parameters
        ----------
        new_core_attr_subset_candidate : `dict`
            A `dict` object.
        skip_validation_and_conversion : `bool`
            Let ``core_attrs`` and ``validation_and_conversion_funcs`` denote
            the attributes
            :attr:`fancytypes.PreSerializableAndUpdatable.core_attrs` and
            :attr:`fancytypes.PreSerializableAndUpdatable.validation_and_conversion_funcs`
            respectively, which are both `dict` objects.

            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``core_attrs`` that is also in
            ``new_core_attr_subset_candidate``, ``core_attrs[key]`` is set to
            ``validation_and_conversion_funcs[key]
            (new_core_attr_subset_candidate)``.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then for each key ``key`` in ``core_attrs`` that is also in
            ``new_core_attr_subset_candidate``, ``core_attrs[key]`` is set to
            ``new_core_attr_subset_candidate[key]``. This option is desired
            primarily when the user wants to avoid potentially expensive copies
            and/or conversions of the `dict` values of
            ``new_core_attr_subset_candidate``, as it is guaranteed that no
            copies or conversions are made in this case.

        """
        kwargs = \
            {"skip_validation_and_conversion": \
             skip_validation_and_conversion,
             "new_core_attr_subset_candidate": \
             new_core_attr_subset_candidate,
             "old_core_attr_set": \
             self._core_attrs,
             "validation_and_conversion_funcs": \
             self._validation_and_conversion_funcs}
        self._core_attrs = \
            _update_old_core_attr_set_and_return_new_core_attr_set(**kwargs)

        return None



    def get_core_attrs(self, deep_copy=_default_deep_copy):
        r"""Return the core attributes.

        Parameters
        ----------
        deep_copy : `bool`
            If ``deep_copy`` is set to ``True``, then a deep copy of the 
            original `dict` representation of the core attributes are returned. 
            Otherwise, a reference to the `dict` representation is returned.

        Returns
        -------
        core_attrs : `dict`
            A `dict` representation of the core attributes: each `dict` key is a
            `str` representing the name of a core attribute, and the 
            corresponding `dict` value is the object to which said core 
            attribute is set.

        """
        params = {"deep_copy": deep_copy}
        deep_copy = _check_and_convert_deep_copy(params)
        
        core_attrs = (self.core_attrs
                      if (deep_copy == True)
                      else self._core_attrs)

        return core_attrs



###########################
## Define error messages ##
###########################

_check_and_convert_validation_and_conversion_funcs_err_msg_1 = \
    ("The object ``validation_and_conversion_funcs`` must be a dictionary with "
     "values set to only callable objects.")

_check_and_convert_core_attrs_candidate_err_msg_1 = \
    ("The objects ``{}`` and ``validation_and_conversion_funcs`` must have "
     "matching key sets.")

_preliminary_check_of_pre_serialization_funcs_err_msg_1 = \
    ("The objects ``pre_serialization_funcs`` and "
     "``validation_and_conversion_funcs`` must have matching key sets.")
_preliminary_check_of_pre_serialization_funcs_err_msg_2 = \
    ("The objects ``pre_serialization_funcs`` must be a dictionary with values "
     "set to only callable objects.")

_preliminary_check_of_de_pre_serialization_funcs_err_msg_1 = \
    ("The objects ``de_pre_serialization_funcs`` and "
     "``validation_and_conversion_funcs`` must have matching key sets.")
_preliminary_check_of_de_pre_serialization_funcs_err_msg_2 = \
    ("The objects ``de_pre_serialization_funcs`` must be a dictionary with "
     "values set to only callable objects.")

_pre_serializable_err_msg_1 = \
    ("An error occurred in testing the instance method ``pre_serialize``: see "
     "the remaining traceback for details.")
_pre_serializable_err_msg_2 = \
    ("An error occurred in testing part of the de-pre-serialization process of "
     "the class: see the remaining traceback for details.")
_pre_serializable_err_msg_3 = \
    ("The object ``serializable_rep`` is missing the key ``'{}'``.")
_pre_serializable_err_msg_4 = \
    ("An error occurred in attempting to de-pre-serialize the object "
     "``serializable_rep``.")
_pre_serializable_err_msg_5 = \
    ("Failed to perform de-pre-serialization: see the remaining traceback for "
     "details.")
_pre_serializable_err_msg_6 = \
    ("Cannot save the serialized representation to a file at the path ``'{}'`` "
     "because a file already exists there and the object ``overwrite`` was set "
     "to ``False``, which prohibits overwriting the original file.")
_pre_serializable_err_msg_7 = \
    ("An error occurred in trying to save the serialized representation to the "
     "file at the path ``'{}'``: see the traceback for details.")
_pre_serializable_err_msg_8 = \
    ("The object ``serialized_rep`` must be a valid JSON document.")
_pre_serializable_err_msg_9 = \
    ("The filename ``'{}'`` is invalid: see the traceback for details.")
