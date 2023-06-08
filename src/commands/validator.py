from typing import Dict, Callable, List

from .logger import Logger, OperationType

"""
    validations looks like this:

    [
        {
            "param_name": "param1",
            "obligatory": True,
            "validator": lambda x: x == "value1"
        },
        ...
    ]

    """


class ParamValidator:

    def __init__(self, command_name: str, validations: List[Dict[str, any]]):

        self.command_name = command_name

        self._validations = [
            Validator(validation) for validation in validations
        ]

        self._obligatory = [
            validation for validation in self._validations if validation.obligatory
        ]

    def validate(self,  params: dict[str, str]):

        errors = []
        warnings = []

        # check obligatory params
        for validation_obj in self._obligatory:
            if validation_obj.param_name not in params:
                errors.append(f"El parametro {validation_obj.param_name} es obligatorio")
                params[validation_obj.param_name] = None  # add param to params as None

        # check params validator functions
        for validation_obj in self._validations:
            if validation_obj.param_name in params:
                if not validation_obj.validator(params[validation_obj.param_name]):
                    errors.append(f"El parametro {validation_obj.param_name} es invalido")

        # unnecessary params
        for param_name in params:
            if param_name not in [validation_obj.param_name for validation_obj in self._validations]:
                warnings.append(f"El parametro {param_name} no es necesario")
                del params[param_name]  # remove param from params

        # Add logs

        command_description = f"En el comando '{self.command_name}': "

        for error in [command_description+error for error in errors]:
            Logger.error(error, OperationType.INPUT)

        for warning in [command_description+warning for warning in warnings]:
            Logger.warning(warning, OperationType.INPUT)

        if len(errors) > 0:
            return False

        # No errors, run command
        return True


class Validator:

    def __init__(self, validation: Dict[str, any]):

        # check if validation["obligatory"] is a bool
        if not isinstance(validation["obligatory"], bool):
            raise Exception(f"Invalid obligatory {validation['obligatory']}")

        # check if validation["param_name"] is a str
        if not isinstance(validation["param_name"], str):
            raise Exception(f"Invalid param_name {validation['param_name']}")

        # check if validation["validator"] is a lambda
        if not isinstance(validation["validator"], Callable):
            raise Exception(f"Invalid validator {validation['validator']}")

        try:
            self.obligatory: bool = validation["obligatory"]
            self.param_name: str = validation["param_name"]
            self.validator: Callable = validation["validator"]
        except KeyError as e:
            raise Exception(f"Invalid validation {validation}") from e
