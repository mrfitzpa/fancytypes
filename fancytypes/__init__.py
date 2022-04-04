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



# For validating objects.
import czekitout.check



# Import child modules and packages of current package.
import fancytypes.version



############################
## Authorship information ##
############################

__author__       = "Matthew Fitzpatrick"
__copyright__    = "Copyright 2022"
__credits__      = ["Matthew Fitzpatrick"]
__version__      = fancytypes.version.version
__full_version__ = fancytypes.version.full_version
__maintainer__   = "Matthew Fitzpatrick"
__email__        = "mrfitzpa@uvic.ca"
__status__       = "Development"



###################################
## Useful background information ##
###################################

# See e.g. ``https://docs.python.org/3/reference/import.html#regular-packages``
# for a brief discussion of ``__init__.py`` files.



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["show_config",
           "Checkable",
           "Updatable",
           "PreSerializable",
           "PreSerializableAndUpdatable"]



def show_config():
    """Print information about the version of ``fancytypes`` and libraries it 
    uses.

    """
    print(version.version_summary)

    return None



class Checkable():
    r"""A type with read-only core attributes that enforces validation upon
    construction.

    Parameters
    ----------
    ctor_params : `dict`
        A `dict` representation of the construction parameters: each `dict` key
        is a `str` representing the name of a construction parameter, and the
        corresponding `dict` value is the object to which said construction
        parameter is set. During construction, each construction parameter is
        potentially converted, and then subsequently set to a so-called "core
        attribute".
    validation_and_conversion_funcs : `dict`
        A `dict` storing validation and conversion functions to be applied to
        the construction parameters: for each `dict` key ``ctor_param_name`` in
        ``ctor_params``, ``validation_and_conversion_funcs[ctor_param_name]``
        yields the validation and conversion function to be applied to the
        construction parameter object ``ctor_params[ctor_param_name]``. Note
        that the `dict` keys of ``validation_and_conversion_funcs`` must match
        those exactly of ``ctor_params``. Furthermore, for each `dict` key
        ``ctor_param_name``,
        ``validation_and_conversion_funcs[ctor_param_name]`` should take
        ``ctor_params`` as the only input argument and return the potentially
        converted construction parameter with the name specified by
        ``ctor_param_name``.
    
    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set.

    """
    def __init__(self, ctor_params, validation_and_conversion_funcs):
        czekitout.check.if_dict_like(ctor_params, "ctor_params")
        czekitout.check.if_dict_like(validation_and_conversion_funcs,
                                     "validation_and_conversion_funcs")
        
        ctor_param_names = sorted(list(validation_and_conversion_funcs.keys()))
        if ctor_param_names != sorted(list(ctor_params.keys())):
            raise KeyError(_checkable_err_msg_1)

        self._core_attrs = dict()
        for ctor_param_name in ctor_param_names:
            if not callable(validation_and_conversion_funcs[ctor_param_name]):
                raise TypeError(_checkable_err_msg_2)
            core_attr = \
                validation_and_conversion_funcs[ctor_param_name](ctor_params)
            self._core_attrs[ctor_param_name] = core_attr

        self._validation_and_conversion_funcs = validation_and_conversion_funcs

        return None



    @property
    def core_attrs(self):
        return copy.deepcopy(self._core_attrs)



class Updatable():
    r"""A type with updatable core attributes that enforces validation upon
    constructing or updating an instance of said type.

    Parameters
    ----------
    checkable_obj : :class:`fancytypes.Checkable`
        A "checkable" object, which stores the updatable core attributes and
        enforces validation.

    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set. Note
        that it is only the core attributes which can be updated directly.
    """
    def __init__(self, checkable_obj):
        kwargs = {"obj": checkable_obj,
                  "obj_name": "checkable_obj",
                  "accepted_types": (Checkable,)}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)
        self._checkable_obj = checkable_obj

        return None



    def update(self, core_attr_subset):
        r"""Update a subset of the core attributes.

        Upon updating the subset of core attributes, the validation and
        conversion functions specified in the construction parameter
        ``checkable_obj`` are applied. See the documentation for the class
        :class:`fancytypes.Checkable`, namely the description of the
        construction parameter ``validation_and_conversion_funcs`` of that
        class, for a discussion on the validation and conversion functions.

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

        """
        czekitout.check.if_dict_like(core_attr_subset, "core_attr_subset")
        core_attrs = core_attr_subset.copy()

        names_of_core_attrs_to_update = core_attr_subset.keys()

        for core_attr_name in self._checkable_obj.core_attrs.keys():
            if core_attr_name not in core_attr_subset:
                core_attrs[core_attr_name] = \
                    self._checkable_obj.core_attrs[core_attr_name]

        for core_attr_name in names_of_core_attrs_to_update:
            if core_attr_name not in self._checkable_obj.core_attrs:
                del core_attrs[core_attr_name]

        validation_and_conversion_funcs = \
            self._checkable_obj._validation_and_conversion_funcs

        self._checkable_obj = Checkable(core_attrs,
                                        validation_and_conversion_funcs)

        return None



    @property
    def core_attrs(self):
        return self._checkable_obj.core_attrs



class PreSerializable():
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

    """
    def __init__(self, ctor_params):
        validation_and_conversion_funcs = self._validation_and_conversion_funcs
        pre_serialization_funcs = self._pre_serialization_funcs
        de_pre_serialization_funcs = self._de_pre_serialization_funcs

        checkable_obj = Checkable(ctor_params, validation_and_conversion_funcs)

        czekitout.check.if_dict_like(pre_serialization_funcs,
                                     "pre_serialization_funcs")
        
        core_attr_names = sorted(list(pre_serialization_funcs.keys()))
        
        if core_attr_names != sorted(list(checkable_obj.core_attrs.keys())):
            raise KeyError(_pre_serializable_err_msg_1)
        for core_attr_name in checkable_obj.core_attrs:
            if not callable(pre_serialization_funcs[core_attr_name]):
                raise TypeError(_pre_serializable_err_msg_2)

        czekitout.check.if_dict_like(de_pre_serialization_funcs,
                                     "de_pre_serialization_funcs")
        core_attr_names = sorted(list(de_pre_serialization_funcs.keys()))
        
        if core_attr_names != sorted(list(checkable_obj.core_attrs.keys())):
            raise KeyError(_pre_serializable_err_msg_3)
        for core_attr_name in core_attr_names:
            if not callable(de_pre_serialization_funcs[core_attr_name]):
                raise TypeError(_pre_serializable_err_msg_4)
        
        self._checkable_obj = checkable_obj

        try:
            serializable_rep = self.pre_serialize()
        except:
            raise ValueError(_pre_serializable_err_msg_5)

        try:
            construct_ctor_params_from_serializable_rep = \
                self._construct_ctor_params_from_serializable_rep
            ctor_params = \
                construct_ctor_params_from_serializable_rep(serializable_rep)
            Checkable(ctor_params, validation_and_conversion_funcs)
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
                ctor_params[ctor_param_name] = de_pre_serialize(datasubset)
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
        for core_attr_name, core_attr in self.core_attrs.items():
            _pre_serialize = self._pre_serialization_funcs[core_attr_name]
            datasubset = _pre_serialize(core_attr)
            data[core_attr_name] = datasubset

        serializable_rep = data

        return serializable_rep



    @property
    def core_attrs(self):
        return self._checkable_obj.core_attrs



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

    """
    def __init__(self, ctor_params):
        PreSerializable.__init__(self, ctor_params)
        
        self._updatable_obj = Updatable(self._checkable_obj)
        
        return None



    def update(self, core_attr_subset):
        r"""Update a subset of the core attributes.

        Upon updating the subset of core attributes, the validation and
        conversion functions specified in the private class attribute
        ``_validation_and_conversion_funcs`` are applied. See the preamble of
        the documentation for the class
        :class:`fancytypes.PreSerializableAndUpdatable` for a discussion on the
        validation and conversion functions.

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

        """
        self._updatable_obj.update(core_attr_subset)
        
        ctor_params = self._updatable_obj.core_attrs
        self._checkable_obj = Checkable(ctor_params,
                                        self._validation_and_conversion_funcs)

        return None



###########################
## Define error messages ##
###########################

_checkable_err_msg_1 = \
    ("The parameters ``ctor_params`` and ``validation_and_conversion_funcs`` "
     "have mismatching key sets.")

_checkable_err_msg_2 = \
    ("The parameter ``validation_and_conversion_funcs`` must be a dictionary "
     "with values set to only callable objects.")

_pre_serializable_err_msg_1 = \
    ("The parameter ``ctor_params`` and the private class attribute "
     "``_pre_serialization_funcs`` have mismatching key sets.")

_pre_serializable_err_msg_2 = \
    ("The private class attribute ``_pre_serialization_funcs`` must be a "
     "dictionary with values set to only callable objects.")

_pre_serializable_err_msg_3 = \
    ("The parameter ``ctor_params`` and the private class attribute "
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
    ("The parameter ``serializable_rep`` is missing the key ``'{}'``.")

_pre_serializable_err_msg_8 = \
    ("An error occurred in attempting to construct the parameter ``{}`` from "
     "a serializable representation.")
