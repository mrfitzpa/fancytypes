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



def _check_and_convert_skip_validation_and_conversion(params):
    obj_name = "skip_validation_and_conversion"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    skip_validation_and_conversion = czekitout.convert.to_bool(**kwargs)

    return skip_validation_and_conversion



_default_skip_validation_and_conversion = False



class Checkable():
    r"""A type with read-only core attributes that enforces validation upon
    construction if specified.

    Parameters
    ----------
    ctor_params : `dict`
        A `dict` representation of the construction parameters: each `dict` key
        is a `str` representing the name of a construction parameter, and the
        corresponding `dict` value is the object to which said construction
        parameter is set. During construction, each construction parameter is
        potentially converted, and then subsequently set to a so-called "core
        attribute".
    skip_validation_and_conversion : `bool`
        If ``skip_validation_and_conversion`` is set to ``False``, then the
        validation and conversion functions specified in
        :attr:`fancytypes.Updatable.validation_and_conversion_funcs` are
        applied to the construction parameters ``ctor_params``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then the validation and conversion steps are skipped. This option is
        desired primarily when the user wants to avoid potentially expensive
        copies and/or conversions of the `dict` values of ``ctor_params``, as no
        copies or conversions are made in this case.
    
    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set.
    validation_and_conversion_funcs : `dict`, read-only
        A `dict` storing validation and conversion functions that are applied to
        the construction parameters ``ctor_params``: for each `dict` key
        ``ctor_param_name`` in ``ctor_attrs``,
        ``validation_and_conversion_funcs[ctor_param_name]`` yields the
        validation and conversion function that is applied to the construction
        parameter object ``ctor_params[ctor_param_name]``. Note that the `dict`
        keys of ``validation_and_conversion_funcs`` must match those exactly of
        ``ctor_attrs``. Furthermore, for each `dict` key ``ctor_param_name``,
        ``validation_and_conversion_funcs[ctor_param_name]`` should take
        ``ctor_params`` as the only input argument and return the potentially
        converted construction parameter with the name specified by
        ``ctor_param_name``.

    """
    def __init__(self,
                 ctor_params,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        params = \
            {"skip_validation_and_conversion": skip_validation_and_conversion}
        skip_validation_and_conversion = \
            _check_and_convert_skip_validation_and_conversion(params)

        if (skip_validation_and_conversion == False):
            self._check_ctor_params_and_set_core_attrs(ctor_params)
        else:
            self._core_attrs = ctor_params

        return None



    def _check_ctor_params_and_set_core_attrs(self, ctor_params):
        kwargs = {"obj": self._validation_and_conversion_funcs,
                  "obj_name": "_validation_and_conversion_funcs"}
        czekitout.check.if_dict_like(**kwargs)

        kwargs = {"obj": ctor_params, "obj_name": "ctor_params"}
        czekitout.check.if_dict_like(**kwargs)

        validation_and_conversion_funcs = \
            self._validation_and_conversion_funcs
        
        ctor_param_names = sorted(list(validation_and_conversion_funcs.keys()))
        if ctor_param_names != sorted(list(ctor_params.keys())):
            raise KeyError(_checkable_err_msg_1)

        self._core_attrs = dict()
        for ctor_param_name in ctor_param_names:
            validation_and_conversion_func = \
                validation_and_conversion_funcs[ctor_param_name]
            if not callable(validation_and_conversion_func):
                raise TypeError(_checkable_err_msg_2)
            core_attr = \
                validation_and_conversion_func(params=ctor_params)
            self._core_attrs[ctor_param_name] = \
                core_attr

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
        new_core_attr_subset,
        old_core_attr_set,
        validation_and_conversion_funcs):
    params = \
        {"skip_validation_and_conversion": skip_validation_and_conversion}
    skip_validation_and_conversion = \
        _check_and_convert_skip_validation_and_conversion(params)

    kwargs = {"obj": new_core_attr_subset, "obj_name": "core_attr_subset"}
    czekitout.check.if_dict_like(**kwargs)
    
    new_core_attr_set = new_core_attr_subset.copy()

    for core_attr_name in old_core_attr_set.keys():
        if core_attr_name not in new_core_attr_subset:
            new_core_attr = old_core_attr_set[core_attr_name]
            new_core_attr_set[core_attr_name] = new_core_attr

    names_of_core_attrs_to_update = tuple()
    for core_attr_name in new_core_attr_subset.keys():
        if core_attr_name not in old_core_attr_set:
            del new_core_attr_set[core_attr_name]
        else:
            names_of_core_attrs_to_update += (core_attr_name,)

    for ctor_param_name in names_of_core_attrs_to_update:
        validation_and_conversion_func = \
            self._validation_and_conversion_funcs[ctor_param_name]

        if (skip_validation_and_conversion == False):
            kwargs = {"params": new_core_attr_set}
            new_core_attr = validation_and_conversion_func(**kwargs)
            new_core_attr_set[ctor_param_name] = new_core_attr

    return new_core_attr_set



def _check_and_convert_deep_copy(params):
    obj_name = "deep_copy"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    deep_copy = czekitout.convert.to_bool(**kwargs)

    return deep_copy



_default_deep_copy = True



class Updatable(Checkable):
    r"""A type with updatable core attributes that enforces validation upon
    constructing or updating an instance of said type.

    Parameters
    ----------
    ctor_params : `dict`
        A `dict` representation of the construction parameters: each `dict` key
        is a `str` representing the name of a construction parameter, and the
        corresponding `dict` value is the object to which said construction
        parameter is set. During construction, each construction parameter is
        potentially converted, and then subsequently set to a so-called "core
        attribute".
    skip_validation_and_conversion : `bool`
        If ``skip_validation_and_conversion`` is set to ``False``, then the
        validation and conversion functions specified in
        :attr:`fancytypes.Updatable.validation_and_conversion_funcs` are
        applied to the construction parameters ``ctor_params``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then the validation and conversion steps are skipped. This option is
        desired primarily when the user wants to avoid potentially expensive
        copies and/or conversions of the `dict` values of ``ctor_params``, as no
        copies or conversions are made in this case.

    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set. Note
        that it is only the core attributes which can be updated directly.
    validation_and_conversion_funcs : `dict`, read-only
        A `dict` storing validation and conversion functions that are applied to
        the construction parameters ``ctor_params`` and to any of the core
        attributes that are to be updated: for each `dict` key
        ``ctor_param_name`` in ``ctor_attrs``,
        ``validation_and_conversion_funcs[ctor_param_name]`` yields the
        validation and conversion function that is applied to the construction
        parameter object ``ctor_params[ctor_param_name]``. Note that the `dict`
        keys of ``validation_and_conversion_funcs`` must match those exactly of
        ``ctor_attrs``. Furthermore, for each `dict` key ``ctor_param_name``,
        ``validation_and_conversion_funcs[ctor_param_name]`` should take
        ``ctor_params`` or ``core_attrs`` as the only input argument and return
        the potentially converted construction parameter or core attribute with
        the name specified by ``ctor_param_name``.

    """
    def __init__(self,
                 ctor_params,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        Checkable.__init__(self, ctor_params, skip_validation_and_conversion)

        return None



    def update(self,
               core_attr_subset,
               skip_validation_and_conversion=\
               _default_skip_validation_and_conversion):
        r"""Update a subset of the core attributes.

        Parameters
        ----------
        core_attr_subset : `dict`
            A `dict` specifying how to update a subset of the core attributes:
            each `dict` key of ``core_attr_subset`` that is also a key of the
            instance attribute :attr:`fancytypes.Updatable.core_attrs` is a
            `str` representing the name of a core attribute, and the
            corresponding `dict` value is the object to which said core
            attribute is to be set. Any `dict` keys of ``core_attr_subset`` that
            are not keys of the instance attribute
            :attr:`fancytypes.Updatable.core_attrs` are ignored in the update
            procedure along with the corresponding `dict` values.
        skip_validation_and_conversion : `bool`
            If ``skip_validation_and_conversion`` is set to ``False``, then a
            upon updating the subset of core attributes, the corresponding
            validation and conversion functions specified in
            :attr:`fancytypes.Updatable.validation_and_conversion_funcs` are
            applied. 

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then the validation and conversion steps are skipped. This option is
            desired primarily when the user wants to avoid potentially expensive
            copies and/or conversions of the `dict` values of
            ``core_attr_subset``, as no copies or conversions are made in this
            case.

        """
        kwargs = \
            {"skip_validation_and_conversion": \
             skip_validation_and_conversion,
             "new_core_attr_subset": \
             core_attr_subset,
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
        core_attrs = (self.core_attrs
                      if (deep_copy == True)
                      else self._core_attrs)

        return core_attrs



def _check_and_convert_overwrite(params):
    obj_name = "overwrite"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    overwrite = czekitout.convert.to_bool(**kwargs)

    return overwrite



_default_overwrite = False



class PreSerializable(Checkable):
    r"""A type that is pre-serializable, that can be constructed from a 
    serializable representation, and that enforces validation upon construction.

    We define pre-serialization as the process of converting an object into a
    form that can be subsequently serialized into a JSON format. We refer to
    objects resulting from pre-serialization as serializable objects.

    We define de-pre-serialization as the process of converting a serializable
    object into its original type, i.e. de-pre-serialization is the reverse
    process of pre-serialization.

    **Note**: One cannot create instances of :class:`fancytypes.PreSerializable`
    without throwing an error. In order to make proper use of the
    :class:`fancytypes.PreSerializable` class, one must define a subclass which
    inherits from it and set three private class attributes in the definition:
    ``_validation_and_conversion_funcs``, ``_pre_serialization_funcs``, and
    ``_de_pre_serialization_funcs``. 

    ``_validation_and_conversion_funcs`` is a `dict` storing validation and
    conversion functions to be applied to the construction parameters
    [represented by the `dict` ``ctor_params`` below]: for each `dict` key
    ``ctor_param_name`` in ``ctor_params``,
    ``_validation_and_conversion_funcs[ctor_param_name]`` yields the validation
    and conversion function to be applied to the construction parameter object
    ``ctor_params[ctor_param_name]``. Note that the `dict` keys of
    ``_validation_and_conversion_funcs`` must match those exactly of
    ``ctor_params``. Furthermore, for each `dict` key ``ctor_param_name``,
    ``_validation_and_conversion_funcs[ctor_param_name]`` should take
    ``ctor_params`` as the only input argument and return the potentially
    converted construction parameter with the name specified by
    ``ctor_param_name``.

    ``_pre_serialization_funcs`` is a `dict` storing pre-serialization functions
    to be applied to the core attributes [represented by the instance attribute
    :attr:`fancytypes.PreSerializable.core_attrs` introduced below]: for each
    `dict` key ``core_attr_name`` in
    :attr:`fancytypes.PreSerializable.core_attrs` [the latter of which we denote
    here as ``core_attrs``], ``_pre_serialization_funcs[core_attr_name]`` yields
    the pre-serialization function to be applied to the core attribute
    ``core_attrs[core_attr_name]``, upon calling the method
    :meth:`fancytypes.PreSerializable.pre_serialize`. Note that the `dict` keys
    of ``_pre_serialization_funcs`` must match those exactly of ``core_attrs``
    and ``ctor_params``. Furthermore, for each `dict` key ``core_attr_name``,
    ``_pre_serialization_funcs[core_attr_name]`` should take ``core_attrs`` as
    the only input argument and return the serializable representation of the
    core attribute with the name specified by ``core_attr_name``.

    ``_de_pre_serialization_funcs`` is a `dict` storing de-pre-serialization
    functions to be applied to serializable representations of the core
    attributes of any instance of the :class:`fancytypes.PreSerializable` class
    or subclass: for each `dict` key ``core_attr_name`` in ``core_attrs``,
    ``_de_pre_serialization_funcs[core_attr_name]`` yields the
    de-pre-serialization function to be applied to the serializable
    representation of the core attribute with the name specified by
    ``core_attr_name``, upon calling the class method
    :meth:`fancytypes.PreSerializable.de_pre_serialize`. Note that the `dict`
    keys of ``_de_pre_serialization_funcs`` must match those exactly of
    ``core_attrs`` and ``ctor_params``. Furthermore, for each `dict` key
    ``core_attr_name``, ``_de_pre_serialization_funcs[core_attr_name]`` should
    take the serializable representation of the core attribute with the name
    specified by ``core_attr_name`` as the only input argument and return the
    de-serialized form of said core attribute.

    Parameters
    ----------
    ctor_params : `dict`
        A `dict` representation of the construction parameters: each `dict` key
        is a `str` representing the name of a construction parameter, and the
        corresponding `dict` value is the object to which said construction
        parameter is set. During construction, each construction parameter is
        potentially converted, and then subsequently set to a so-called "core
        attribute".
    skip_validation_and_conversion : `bool`
        If ``skip_validation_and_conversion`` is set to ``False``, then the
        validation and conversion functions specified in
        :attr:`fancytypes.Updatable.validation_and_conversion_funcs` are
        applied to the construction parameters ``ctor_params``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then the validation and conversion steps are skipped. This option is
        desired primarily when the user wants to avoid potentially expensive
        copies and/or conversions of the `dict` values of ``ctor_params``, as no
        copies or conversions are made in this case.

    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set.

        **Note**: If the currently documented class, which we denote here as
        ``cls``, is neither :class:`PreSerializable` nor
        :class:`PreSerializableAndUpdatable`, then in order for ``cls`` to be
        well-behaved, it must satisfy ``instance.core_attrs ==
        cls(**instance.core_attrs).core_attrs``, where ``instance`` is any
        instance of ``cls`` that was constructed without error.
    validation_and_conversion_funcs : `dict`, read-only
        A `dict` storing validation and conversion functions that are applied to
        the construction parameters ``ctor_params``: for each `dict` key
        ``ctor_param_name`` in ``ctor_attrs``,
        ``validation_and_conversion_funcs[ctor_param_name]`` yields the
        validation and conversion function that is applied to the construction
        parameter object ``ctor_params[ctor_param_name]``. Note that the `dict`
        keys of ``validation_and_conversion_funcs`` must match those exactly of
        ``ctor_attrs``. Furthermore, for each `dict` key ``ctor_param_name``,
        ``validation_and_conversion_funcs[ctor_param_name]`` should take
        ``ctor_params`` as the only input argument and return the potentially
        converted construction parameter with the name specified by
        ``ctor_param_name``.
    pre_serialization_funcs : `dict`, read-only
        A `dict` storing pre-serialization functions that are applied to the
        core attributes ``core_attrs``: for each `dict` key ``core_attr_name``
        in ``core_attrs``, ``pre_serialization_funcs[core_attr_name]`` yields
        the pre-serialization function that is applied to the core attribute
        ``core_attrs[core_attr_name]``, upon calling the method
        :meth:`fancytypes.PreSerializable.pre_serialize`. Note that the `dict`
        keys of ``pre_serialization_funcs`` must match those exactly of
        ``core_attrs``. Furthermore, for each `dict` key ``core_attr_name``,
        ``pre_serialization_funcs[core_attr_name]`` should take ``core_attrs``
        as the only input argument and return the serializable representation of
        the core attribute with the name specified by ``core_attr_name``.
    de_pre_serialization_funcs : `dict`, read-only
        A `dict` storing de-pre-serialization functions that are applied to
        serializable representations of the core attributes ``core_attrs``: for
        each `dict` key ``core_attr_name`` in ``core_attrs``,
        ``de_pre_serialization_funcs[core_attr_name]`` yields the
        de-pre-serialization function that is applied to the serializable
        representation of the core attribute ``core_attrs[core_attr_name]``,
        upon calling the method
        :meth:`fancytypes.PreSerializable.de_pre_serialize`. Note that the
        `dict` keys of ``de_pre_serialization_funcs`` must match those exactly
        of ``core_attrs``. Furthermore, for each `dict` key ``core_attr_name``,
        ``de_pre_serialization_funcs[core_attr_name]`` should take the
        serializable representation of the core attribute with the name
        specified by ``core_attr_name`` as the only input argument and return
        the de-serialized form of said core attribute.

    """
    def __init__(self,
                 ctor_params,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        Checkable.__init__(self, ctor_params, skip_validation_and_conversion)

        kwargs = {"obj": self._pre_serialization_funcs,
                  "obj_name": "_pre_serialization_funcs"}
        czekitout.check.if_dict_like(**kwargs)

        kwargs = {"obj": self._de_pre_serialization_funcs,
                  "obj_name": "_de_pre_serialization_funcs"}
        czekitout.check.if_dict_like(**kwargs)

        validation_and_conversion_funcs = self._validation_and_conversion_funcs
        pre_serialization_funcs = self._pre_serialization_funcs
        de_pre_serialization_funcs = self._de_pre_serialization_funcs
        
        core_attr_names = sorted(list(pre_serialization_funcs.keys()))
        
        if core_attr_names != sorted(list(self._core_attrs.keys())):
            raise KeyError(_pre_serializable_err_msg_1)
        for core_attr_name in self._core_attrs:
            if not callable(pre_serialization_funcs[core_attr_name]):
                raise TypeError(_pre_serializable_err_msg_2)

        core_attr_names = sorted(list(de_pre_serialization_funcs.keys()))
        
        if core_attr_names != sorted(list(self._core_attrs.keys())):
            raise KeyError(_pre_serializable_err_msg_3)
        for core_attr_name in core_attr_names:
            if not callable(de_pre_serialization_funcs[core_attr_name]):
                raise TypeError(_pre_serializable_err_msg_4)

        if (skip_validation_and_conversion == False):
            try:
                serializable_rep = self.pre_serialize()
            except:
                raise ValueError(_pre_serializable_err_msg_5)
        
            try:
                construct_ctor_params = \
                    self._construct_ctor_params_from_serializable_rep
                
                ctor_params = construct_ctor_params(serializable_rep)
                self._check_ctor_params_and_set_core_attrs(ctor_params)
            except:
                raise ValueError(_pre_serializable_err_msg_6)
        
        return None



    @classmethod
    def _construct_ctor_params_from_serializable_rep(cls, serializable_rep):
        ctor_params = dict()
        
        validation_and_conversion_funcs = cls._validation_and_conversion_funcs
        
        de_pre_serialization_funcs = cls._de_pre_serialization_funcs
        ctor_param_names = sorted(list(de_pre_serialization_funcs.keys()))
        
        czekitout.check.if_dict_like(serializable_rep, "serializable_rep")
        for ctor_param_name in ctor_param_names:
            if ctor_param_name not in serializable_rep:
                err_msg = _pre_serializable_err_msg_7.format(ctor_param_name)
                raise KeyError(err_msg)
        data = serializable_rep

        try:
            for ctor_param_name in ctor_param_names:
                datasubset = data[ctor_param_name]
                de_pre_serialize = de_pre_serialization_funcs[ctor_param_name]
                ctor_param = copy.deepcopy(de_pre_serialize(datasubset))
                ctor_params[ctor_param_name] = ctor_param
        except:
            err_msg = _pre_serializable_err_msg_8.format(ctor_param_name)
            raise ValueError(err_msg)

        return ctor_params



    @classmethod
    def de_pre_serialize(cls, serializable_rep):
        r"""Construct an instance from a serializable representation.

        We define pre-serialization as the process of converting an object into
        a form that can be subsequently serialized into a JSON format. We refer
        to objects resulting from pre-serialization as serializable objects.

        We define de-pre-serialization as the process of converting a
        serializable object into its original type, i.e. de-pre-serialization is
        the reverse process of pre-serialization.

        Parameters
        ----------
        serializable_rep : `dict`
            A serializable representation of an instance. Serializable
            representations can be generated using the instance method 
            :meth:`fancytypes.PreSerializable.pre_serialize`.

        Returns
        -------
        pre_serializable_obj : :class:`fancytypes.PreSerializable`
            An instance constructed from the serializable representation
            ``serializable_rep``.
        """
        ctor_params = \
            cls._construct_ctor_params_from_serializable_rep(serializable_rep)

        if (cls is PreSerializable) or (cls is PreSerializableAndUpdatable):
            pre_serializable_obj = cls(ctor_params)
        else:
            pre_serializable_obj = cls(**ctor_params)
                
        return pre_serializable_obj



    def pre_serialize(self):
        r"""Pre-serialize instance.

        We define pre-serialization as the process of converting an object into
        a form that can be subsequently serialized into a JSON format. We refer
        to objects resulting from pre-serialization as serializable objects.

        We define de-pre-serialization as the process of converting a
        serializable object into its original type, i.e. de-pre-serialization is
        the reverse process of pre-serialization.

        Returns
        -------
        serializable_rep : `dict`
            A serializable representation of an instance.

        """
        data = dict()
        for core_attr_name, core_attr in self._core_attrs.items():
            _pre_serialize = self._pre_serialization_funcs[core_attr_name]
            datasubset = copy.deepcopy(_pre_serialize(core_attr))
            data[core_attr_name] = datasubset

        serializable_rep = data

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
        kwargs = {"obj": overwrite, "obj_name": "overwrite"}
        overwrite = czekitout.convert.to_bool(**kwargs)
        
        kwargs = {"obj": filename, "obj_name": "filename"}
        filename = czekitout.convert.to_str_from_path_like(**kwargs)
        if pathlib.Path(filename).is_file():
            if not overwrite:
                raise IOError(_pre_serializable_err_msg_9.format(filename))

        serializable_rep = self.pre_serialize()

        try:
            with open(filename, "w", encoding="utf-8") as file_obj:
                json.dump(serializable_rep,
                          file_obj,
                          ensure_ascii=False,
                          indent=4)
        except:
            raise IOError(_pre_serializable_err_msg_10.format(filename))
            
        return None



    @classmethod
    def loads(cls, serialized_rep):
        r"""Construct an instance from a serialized representation.

        Users can generate serialized representations using the method
        :meth:`fancytypes.PreSerializable.dumps`.

        Parameters
        ----------
        serialized_rep : `str` | `bytes` | `bytearray`
            The serialized representation.

        Returns
        -------
        pre_serializable_obj : :class:`fancytypes.PreSerializable`
            An instance constructed from the serialized representation.

        """
        kwargs = {"obj": serialized_rep,
                  "obj_name": "serialized_rep",
                  "accepted_types": (str, bytes, bytearray)}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)
        
        try:
            serializable_rep = json.loads(serialized_rep)
        except json.decoder.JSONDecodeError:
            raise ValueError(_pre_serializable_err_msg_11)
        except BaseException as err:
            raise err

        pre_serializable_obj = cls.de_pre_serialize(serializable_rep)
                
        return pre_serializable_obj



    @classmethod
    def load(cls, filename):
        r"""Construct an instance from a serialized representation that is 
        stored in a JSON file.

        Users can save serialized representations to JSON files using the method
        :meth:`fancytypes.PreSerializable.dump`.

        Parameters
        ----------
        filename : `str`
            The relative or absolute path to the JSON file that is storing the
            serialized representation of an instance.

        Returns
        -------
        pre_serializable_obj : :class:`fancytypes.PreSerializable`
            An instance constructed from the serialized representation
            stored in the JSON file.

        """
        kwargs = {"obj": filename, "obj_name": "filename"}
        filename = czekitout.convert.to_str_from_path_like(**kwargs)
        
        try:
            with open(filename, 'r') as file_obj:
                serializable_rep = json.load(file_obj)
        except:
            raise IOError(_pre_serializable_err_msg_12.format(filename))

        pre_serializable_obj = cls.de_pre_serialize(serializable_rep)
                
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
    r"""A type with updatable core attributes, that is pre-serializable, that 
    can be constructed from a serializable representation, and that enforces 
    validation upon construction.

    We define pre-serialization as the process of converting an object into a
    form that can be subsequently serialized into a JSON format. We refer to
    objects resulting from pre-serialization as serializable objects.

    We define de-pre-serialization as the process of converting a serializable
    object into its original type, i.e. de-pre-serialization is the reverse
    process of pre-serialization.

    **Note**: One cannot create instances of
    :class:`fancytypes.PreSerializableAndUpdatable` without throwing an
    error. In order to make proper use of the
    :class:`fancytypes.PreSerializableAndUpdatable` class, one must define a
    subclass which inherits from it and set three private class attributes in
    the definition: ``_validation_and_conversion_funcs``,
    ``_pre_serialization_funcs``, and ``_de_pre_serialization_funcs``.

    ``_validation_and_conversion_funcs`` is a `dict` storing validation and
    conversion functions to be applied to the construction parameters
    [represented by the `dict` ``ctor_params`` below]: for each `dict` key
    ``ctor_param_name`` in ``ctor_params``,
    ``_validation_and_conversion_funcs[ctor_param_name]`` yields the validation
    and conversion function to be applied to the construction parameter object
    ``ctor_params[ctor_param_name]``. Note that the `dict` keys of
    ``_validation_and_conversion_funcs`` must match those exactly of
    ``ctor_params``. Furthermore, for each `dict` key ``ctor_param_name``,
    ``_validation_and_conversion_funcs[ctor_param_name]`` should take
    ``ctor_params`` as the only input argument and return the potentially
    converted construction parameter with the name specified by
    ``ctor_param_name``.

    ``_pre_serialization_funcs`` is a `dict` storing pre-serialization functions
    to be applied to the core attributes [represented by the instance attribute
    :attr:`fancytypes.PreSerializableAndUpdatable.core_attrs` introduced below]:
    for each `dict` key ``core_attr_name`` in
    :attr:`fancytypes.PreSerializableAndUpdatable.core_attrs` [the latter of
    which we denote here as ``core_attrs``],
    ``_pre_serialization_funcs[core_attr_name]`` yields the pre-serialization
    function to be applied to the core attribute ``core_attrs[core_attr_name]``,
    upon calling the method
    :meth:`fancytypes.PreSerializableAndUpdatable.pre_serialize`. Note that the
    `dict` keys of ``_pre_serialization_funcs`` must match those exactly of
    ``core_attrs`` and ``ctor_params``. Furthermore, for each `dict` key
    ``core_attr_name``, ``_pre_serialization_funcs[core_attr_name]`` should take
    ``core_attrs`` as the only input argument and return the serializable
    representation of the core attribute with the name specified by
    ``core_attr_name``.

    ``_de_pre_serialization_funcs`` is a `dict` storing de-pre-serialization
    functions to be applied to serializable representations of the core
    attributes of any instance of the
    :class:`fancytypes.PreSerializableAndUpdatable` class or subclass: for each
    `dict` key ``core_attr_name`` in ``core_attrs``,
    ``_de_pre_serialization_funcs[core_attr_name]`` yields the
    de-pre-serialization function to be applied to the serializable
    representation of the core attribute with the name specified by
    ``core_attr_name``, upon calling the class method
    :meth:`fancytypes.PreSerializableAndUpdatable.de_pre_serialize`. Note that
    the `dict` keys of ``_de_pre_serialization_funcs`` must match those exactly
    of ``core_attrs`` and ``ctor_params``. Furthermore, for each `dict` key
    ``core_attr_name``, ``_de_pre_serialization_funcs[core_attr_name]`` should
    take the serializable representation of the core attribute with the name
    specified by ``core_attr_name`` as the only input argument and return the
    de-serialized form of said core attribute.

    Parameters
    ----------
    ctor_params : `dict`
        A `dict` representation of the construction parameters: each `dict` key
        is a `str` representing the name of a construction parameter, and the
        corresponding `dict` value is the object to which said construction
        parameter is set. During construction, each construction parameter is
        potentially converted, and then subsequently set to a so-called "core
        attribute".
    skip_validation_and_conversion : `bool`
        If ``skip_validation_and_conversion`` is set to ``False``, then the
        validation and conversion functions specified in
        :attr:`fancytypes.Updatable.validation_and_conversion_funcs` are
        applied to the construction parameters ``ctor_params``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then the validation and conversion steps are skipped. This option is
        desired primarily when the user wants to avoid potentially expensive
        copies and/or conversions of the `dict` values of ``ctor_params``, as no
        copies or conversions are made in this case.

    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set.

        **Note**: If the currently documented class, which we denote here as
        ``cls``, is neither :class:`PreSerializable` nor
        :class:`PreSerializableAndUpdatable`, then in order for ``cls`` to be
        well-behaved, it must satisfy ``instance.core_attrs ==
        cls(**instance.core_attrs).core_attrs``, where ``instance`` is any
        instance of ``cls`` that was constructed without error.
    validation_and_conversion_funcs : `dict`, read-only
        A `dict` storing validation and conversion functions that are applied to
        the construction parameters ``ctor_params`` and to any of the core
        attributes that are to be updated: for each `dict` key
        ``ctor_param_name`` in ``ctor_attrs``,
        ``validation_and_conversion_funcs[ctor_param_name]`` yields the
        validation and conversion function that is applied to the construction
        parameter object ``ctor_params[ctor_param_name]``. Note that the `dict`
        keys of ``validation_and_conversion_funcs`` must match those exactly of
        ``ctor_attrs``. Furthermore, for each `dict` key ``ctor_param_name``,
        ``validation_and_conversion_funcs[ctor_param_name]`` should take
        ``ctor_params`` or ``core_attrs`` as the only input argument and return
        the potentially converted construction parameter or core attribute with
        the name specified by ``ctor_param_name``.
    pre_serialization_funcs : `dict`, read-only
        A `dict` storing pre-serialization functions that are applied to the
        core attributes ``core_attrs``: for each `dict` key ``core_attr_name``
        in ``core_attrs``, ``pre_serialization_funcs[core_attr_name]`` yields
        the pre-serialization function that is applied to the core attribute
        ``core_attrs[core_attr_name]``, upon calling the method
        :meth:`fancytypes.PreSerializable.pre_serialize`. Note that the `dict`
        keys of ``pre_serialization_funcs`` must match those exactly of
        ``core_attrs``. Furthermore, for each `dict` key ``core_attr_name``,
        ``pre_serialization_funcs[core_attr_name]`` should take ``core_attrs``
        as the only input argument and return the serializable representation of
        the core attribute with the name specified by ``core_attr_name``.
    de_pre_serialization_funcs : `dict`, read-only
        A `dict` storing de-pre-serialization functions that are applied to
        serializable representations of the core attributes ``core_attrs``: for
        each `dict` key ``core_attr_name`` in ``core_attrs``,
        ``de_pre_serialization_funcs[core_attr_name]`` yields the
        de-pre-serialization function that is applied to the serializable
        representation of the core attribute ``core_attrs[core_attr_name]``,
        upon calling the method
        :meth:`fancytypes.PreSerializable.de_pre_serialize`. Note that the
        `dict` keys of ``de_pre_serialization_funcs`` must match those exactly
        of ``core_attrs``. Furthermore, for each `dict` key ``core_attr_name``,
        ``de_pre_serialization_funcs[core_attr_name]`` should take the
        serializable representation of the core attribute with the name
        specified by ``core_attr_name`` as the only input argument and return
        the de-serialized form of said core attribute.

    """
    def __init__(self,
                 ctor_params,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        PreSerializable.__init__(self,
                                 ctor_params,
                                 skip_validation_and_conversion)
        
        return None



    def update(self,
               core_attr_subset,
               skip_validation_and_conversion=\
               _default_skip_validation_and_conversion):
        r"""Update a subset of the core attributes.

        Parameters
        ----------
        core_attr_subset : `dict`
            A `dict` specifying how to update a subset of the core attributes:
            each `dict` key of ``core_attr_subset`` that is also a key of the
            instance attribute
            :attr:`fancytypes.PreSerializableAndUpdatable.core_attrs` is a `str`
            representing the name of a core attribute, and the corresponding
            `dict` value is the object to which said core attribute is to be
            set. Any `dict` keys of ``core_attr_subset`` that are not keys of
            the instance attribute
            :attr:`fancytypes.PreSerializableAndUpdatable.core_attrs` are
            ignored in the update procedure along with the corresponding `dict`
            values.
        skip_validation_and_conversion : `bool`
            If ``skip_validation_and_conversion`` is set to ``False``, then a
            upon updating the subset of core attributes, the corresponding
            validation and conversion functions specified in
            :attr:`fancytypes.PreSerializableAndUpdatable.validation_and_conversion_funcs`
            are applied.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then the validation and conversion steps are skipped. This option is
            desired primarily when the user wants to avoid potentially expensive
            copies and/or conversions of the `dict` values of
            ``core_attr_subset``, as no copies or conversions are made in this
            case.

        """
        kwargs = \
            {"skip_validation_and_conversion": \
             skip_validation_and_conversion,
             "new_core_attr_subset": \
             core_attr_subset,
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
        core_attrs = (self.core_attrs
                      if (deep_copy == True)
                      else self._core_attrs)

        return core_attrs



###########################
## Define error messages ##
###########################

_checkable_err_msg_1 = \
    ("The objects ``ctor_params`` and ``validation_and_conversion_funcs`` have "
     "mismatching key sets.")
_checkable_err_msg_2 = \
    ("The object ``validation_and_conversion_funcs`` must be a dictionary with "
     "values set to only callable objects.")

_pre_serializable_err_msg_1 = \
    ("The object ``ctor_params`` and the private class attribute "
     "``_pre_serialization_funcs`` have mismatching key sets.")
_pre_serializable_err_msg_2 = \
    ("The private class attribute ``_pre_serialization_funcs`` must be a "
     "dictionary with values set to only callable objects.")
_pre_serializable_err_msg_3 = \
    ("The object ``ctor_params`` and the private class attribute "
     "``_de_pre_serialization_funcs`` have mismatching key sets.")
_pre_serializable_err_msg_4 = \
    ("The private class attribute ``_de_pre_serialization_funcs`` must be a "
     "dictionary with values set to only callable objects.")
_pre_serializable_err_msg_5 = \
    ("An error occurred in testing the instance method ``pre_serialize``: see "
     "the remaining traceback for details.")
_pre_serializable_err_msg_6 = \
    ("An error occurred in testing part of the class method "
     "``de_pre_serialize``: see the remaining traceback for details.")
_pre_serializable_err_msg_7 = \
    ("The object ``serializable_rep`` is missing the key ``'{}'``.")
_pre_serializable_err_msg_8 = \
    ("An error occurred in attempting to construct the object ``{}`` from a "
     "serializable representation.")
_pre_serializable_err_msg_9 = \
    ("Cannot save the serialized representation to a file at the path ``'{}'`` "
     "because a file already exists there and the object ``overwrite`` was set "
     "to ``False``, which prohibits overwriting the original file.")
_pre_serializable_err_msg_10 = \
    ("An error occurred in trying to save the serialized representation to the "
     "file at the path ``'{}'``: see the traceback for details.")
_pre_serializable_err_msg_11 = \
    ("The object ``serialized_rep`` must be a valid JSON document.")
_pre_serializable_err_msg_12 = \
    ("The filename ``'{}'`` is invalid: see the traceback for details.")
