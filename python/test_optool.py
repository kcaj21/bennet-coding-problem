import pytest
import responses
import optool


@responses.activate
def test_chemical_name():
    responses.add(
        responses.GET,
        "https://openprescribing.net/api/1.0/bnf_code?q=0407010AD&exact=true&format=json",
        json=[
            {
                "type": "chemical",
                "id": "0407010AD",
                "name": "Paracetamol and ibuprofen",
                "section": "4.7: Analgesics",
            },
        ],
    )
    assert optool.get_chemical_name("0407010AD") == "Paracetamol and ibuprofen"


# @pytest.mark.xfail(reason="not implemented")
def test_not_full_code():
    with pytest.raises(ValueError) as excinfo:
        optool.get_chemical_name("0407010ADAAABAB")
    assert "must be 9 character chemical code" in str(excinfo.value)


# @pytest.mark.xfail(reason="not implemented")
@responses.activate
def test_code_not_present():
    # OpenPrescribing returns an empty list for codes that it doesn't recognise
    responses.add(
        responses.GET,
        "https://openprescribing.net/api/1.0/bnf_code?q=0000000AA&exact=true&format=json",
        json=[],
    )

    with pytest.raises(ValueError) as excinfo:
        optool.get_chemical_name("0000000AA")
    assert "not found" in str(excinfo.value)
    
# @pytest.mark.xfail(reason="not implemented")
@responses.activate
def test_get_icb_spending_data():
    responses.add(
        responses.GET,
        "https://openprescribing.net/api/1.0/spending_by_org/?org_type=icb&code=0407010AD&format=json",
        json=[
            {
                "items": 3,
                "quantity": 68,
                "actual_cost": 10.3,
                "date": "2019-04-02",
                "row_id": "QH8",
                "row_name": "NHS MID AND SOUTH ESSEX INTEGRATED CARE BOARD",
            },
            {
                "items": 1,
                "quantity": 68,
                "actual_cost": 10.3,
                "date": "2019-04-02",
                "row_id": "QH8",
                "row_name": "NHS DERBY AND DERBYSHIRE INTEGRATED CARE BOARD",
            },
            {
                "items":2,
                "quantity":12.0,
                "actual_cost":2.41,
                "date":"2019-04-01",
                "row_id":"QHL",
                "row_name":"NHS BIRMINGHAM AND SOLIHULL INTEGRATED CARE BOARD"
            },
            {
                "items":2,
                "quantity":92.0,
                "actual_cost":13.93,
                "date":"2019-04-01",
                "row_id":"QJ2",
                "row_name":"NHS DERBY AND DERBYSHIRE INTEGRATED CARE BOARD"
            },
        ],
    )
    assert optool.get_icb_spending_data("0407010AD") == [
        '2019-04-02 NHS MID AND SOUTH ESSEX INTEGRATED CARE BOARD 3',
        '2019-04-01 NHS BIRMINGHAM AND SOLIHULL INTEGRATED CARE BOARD 2', 
        '2019-04-01 NHS DERBY AND DERBYSHIRE INTEGRATED CARE BOARD 2'
        ]