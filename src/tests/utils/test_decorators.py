from ak_sap.utils.decorators import smooth_sap_do


def test_smooth_sap_do():
    @smooth_sap_do
    def return_failed_list():
        return [1, 2, 3, 1]

    assert return_failed_list() is None

    @smooth_sap_do
    def return_successful_list():
        return [1, 2, 3, 0]

    assert return_successful_list() == [1, 2, 3]

    @smooth_sap_do
    def return_successful_tuple():
        return [(1, 2, 3), 0]

    assert return_successful_tuple() == (1, 2, 3)

    @smooth_sap_do
    def return_failed_tuple():
        return [(1, 2, 3), 1]

    assert return_failed_tuple() is None

    @smooth_sap_do
    def return_successful_str():
        return ["alpha", 0]

    assert return_successful_str() == "alpha"

    @smooth_sap_do
    def return_failed_str():
        return ["alpha", 1]

    assert return_failed_str() is None

    @smooth_sap_do
    def return_successful_float():
        return [3.14, 0]

    assert return_successful_float() == 3.14

    @smooth_sap_do
    def return_failed_float():
        return [3.14, 1]

    assert return_failed_float() is None

    @smooth_sap_do
    def return_success():
        return 0

    assert return_success() == 0

    @smooth_sap_do
    def return_fail():
        return 1

    assert return_fail() is None
