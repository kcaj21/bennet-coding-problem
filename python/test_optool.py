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
