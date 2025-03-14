# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""An instruction to transmit a given pulse on a ``PulseChannel`` (i.e., those which support
transmitted pulses, such as ``DriveChannel``).
"""
from typing import Optional, Union, Tuple, Set

from qiskit.circuit.parameterexpression import ParameterExpression
from qiskit.pulse.channels import PulseChannel
from qiskit.pulse.exceptions import PulseError
from qiskit.pulse.instructions.instruction import Instruction
from qiskit.pulse.library.pulse import Pulse


class Play(Instruction):
    """This instruction is responsible for applying a pulse on a channel.

    The pulse specifies the exact time dynamics of the output signal envelope for a limited
    time. The output is modulated by a phase and frequency which are controlled by separate
    instructions. The pulse duration must be fixed, and is implicitly given in terms of the
    cycle time, dt, of the backend.
    """

    def __init__(self, pulse: Pulse, channel: PulseChannel, name: Optional[str] = None):
        """Create a new pulse instruction.

        Args:
            pulse: A pulse waveform description, such as
                   :py:class:`~qiskit.pulse.library.Waveform`.
            channel: The channel to which the pulse is applied.
            name: Name of the instruction for display purposes. Defaults to ``pulse.name``.

        Raises:
            PulseError: If pulse is not a Pulse type, or channel is not a PulseChannel.
        """
        if not isinstance(pulse, Pulse):
            raise PulseError("The `pulse` argument to `Play` must be of type `library.Pulse`.")
        if not isinstance(channel, PulseChannel):
            raise PulseError(
                "The `channel` argument to `Play` must be of type `channels.PulseChannel`."
            )
        if name is None:
            name = pulse.name
        super().__init__(operands=(pulse, channel), name=name)

    @property
    def pulse(self) -> Pulse:
        """A description of the samples that will be played."""
        return self.operands[0]

    @property
    def channel(self) -> PulseChannel:
        """Return the :py:class:`~qiskit.pulse.channels.Channel` that this instruction is
        scheduled on.
        """
        return self.operands[1]

    @property
    def channels(self) -> Tuple[PulseChannel]:
        """Returns the channels that this schedule uses."""
        return (self.channel,)

    @property
    def duration(self) -> Union[int, ParameterExpression]:
        """Duration of this instruction."""
        return self.pulse.duration

    @property
    def parameters(self) -> Set:
        """Parameters which determine the instruction behavior."""
        parameters = set()
        for pulse_param_expr in self.pulse.parameters.values():
            if isinstance(pulse_param_expr, ParameterExpression):
                for pulse_param in pulse_param_expr.parameters:
                    parameters.add(pulse_param)
        if self.channel.is_parameterized():
            for ch_param in self.channel.parameters:
                parameters.add(ch_param)

        return parameters

    def is_parameterized(self) -> bool:
        """Return True iff the instruction is parameterized."""
        return self.pulse.is_parameterized() or super().is_parameterized()
