from typing import Literal
import typing


_UNITS_LITERALS = Literal['lb_in_F', 'lb_ft_F', 'kip_in_F', 'kip_ft_F', 'kN_mm_C',
                        'kN_m_C', 'kgf_mm_C', 'kgf_m_C', 'N_mm_C', 'N_m_C',
                        'Ton_mm_C', 'Ton_m_C', 'kN_cm_C', 'kgf_cm_C', 'N_cm_C',
                        'Ton_cm_C']
_UNITS = typing.get_args(_UNITS_LITERALS)

_PROJECT_INFO_KEYS = Literal['Company Name', 'Client Name', 'Project Name', 'Project Number',
                                'Model Name', 'Model Description', 'Revision Number', 'Frame Type',
                                'Engineer', 'Checker', 'Supervisor', 'Issue Code', 'Design Code',]
