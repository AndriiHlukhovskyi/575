from homepage.forms import UnitChoiceForm

from blockexplorer.settings import DEFAULT_USER_UNIT

from blockcypher.constants import UNIT_CHOICES


# speedup since called on every pageload
UNIT_CHOICES_SET = set(UNIT_CHOICES)


def get_user_units(request):

    user_units = DEFAULT_USER_UNIT

    is_eth = "eth" in request.path
    if is_eth and user_units not in ["ether", "gwei", "wei"]:
        user_units = "ether"
    if (not is_eth) and user_units in ["ether", "gwei", "wei"]:
        user_units = DEFAULT_USER_UNIT

    # tcp = template context processor, added to prevent namespace collisions
    return {
            'tcp__user_units': user_units,
            'tcp__unit_choice_form': UnitChoiceForm(initial={'unit_choice': user_units}),
            }
