import pytest

from ak_sap.Analyze.main import case_status, get_run_flag, get_solver

def test_case_status():
    ret = (4, ('Dead', 'Live', 'MODAL', 'Snow'), (1, 2, 3, 4), 0)
    expected = {
        'Dead': 'Not run',
        'Live': 'Could not start',
        'MODAL': 'Not finished',
        'Snow': 'Finished',
    }
    assert case_status(ret) == expected
    
    ret = [1, ('Dead'), (1), 0]
    expected = {
        'Dead': 'Not run',
    }
    assert case_status(ret) == expected
    
    ret = [1, ('Dead'), (1), 1]
    with pytest.raises(AssertionError):
        case_status(ret)
    
def test_get_run_flag():
    ret = [3, ('DEAD', 'Live', 'EQ'), (True, True, False), 0]
    expected= {
        'DEAD': True,
        'Live': True,
        'EQ': False,
    }
    assert get_run_flag(ret) == expected
    
    ret = [1, ('DEAD'), (True), 0]
    expected= {
        'DEAD': True,
    }
    assert get_run_flag(ret) == expected
    
    ret = [1, ('DEAD'), (True), 1]
    with pytest.raises(AssertionError):
        get_run_flag(ret)
    
def test_get_solver():
    ret = [1, 0, 1, -102399, -4, '', 0]
    expected = {'SolverType': 'Advanced',
        'SolverProcessType': 'Auto',
        'NumberParallelRuns': 1,
        'StiffCase': ''}
    assert get_solver(ret) == expected
    
    ret = [0, 1, -2, -102399, -4, 'DEAD', 0]
    expected = {'SolverType': 'Standard',
        'SolverProcessType': 'GUI',
        'NumberParallelRuns': 2,
        'StiffCase': 'DEAD'}
    assert get_solver(ret) == expected
    
    ret = [0, 1, -2, -102399, -4, 'DEAD', 1]
    with pytest.raises(AssertionError):
        get_solver(ret)