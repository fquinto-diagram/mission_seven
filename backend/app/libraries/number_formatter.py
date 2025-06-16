import math
from app.config.translations.i18n import get_translation

class NumberFormatter:
    
    
    def format(number: float | int, decimal_places: int = 2, thousands_separator: str = ".", decimal_separator: str = ",") -> str:
        format_spec = f",.{decimal_places}f"
        formatted = format(number, format_spec)
        if thousands_separator == decimal_separator:
            return formatted
        formatted = formatted.replace(",", "X").replace(".", decimal_separator).replace("X", thousands_separator)
        
        return formatted
        
    def unformat(number: str) -> float:
        """
        Unformats a number string to a float.
        Args:
            number: The number string to unformat.
        Returns:
            The unformatted number as a float.
        """
        number_str = number.strip()
        if "." in number_str and "," in number_str:
            if number_str.rfind(",") > number_str.rfind("."):
                thousands_sep, decimal_sep = ".", ","
            else:
                thousands_sep, decimal_sep = ",", "."
        elif "," in number_str:
            if len(number_str.split(",")[-1]) == 2:
                thousands_sep, decimal_sep = ".", ","
            else:
                thousands_sep, decimal_sep = "", ","
        elif "." in number_str:
            if len(number_str.split(".")[-1]) == 2:
                thousands_sep, decimal_sep = ",", "."
            else:
                thousands_sep, decimal_sep = "", "."
        else:
            return float(number_str)

        clean_str = number_str.replace(thousands_sep, "").replace(decimal_sep, ".")
        return float(clean_str)

def _float_check_precision(precision_digits=None, precision_rounding=None):
    assert (precision_digits is not None or precision_rounding is not None) and \
        not (precision_digits and precision_rounding),\
        get_translation("errors.invalid_float_check_precision")
    assert precision_rounding is None or precision_rounding > 0,\
        get_translation("errors.precision_rounding_must_be_positive", precision_rounding=precision_rounding)
    if precision_digits is not None:
        return 10 ** -precision_digits
    return precision_rounding

def float_round(value, precision_digits=None, precision_rounding=None, rounding_method='HALF-UP'):
    """Return ``value`` rounded to ``precision_digits`` decimal digits,
       minimizing IEEE-754 floating point representation errors, and applying
       the tie-breaking rule selected with ``rounding_method``, by default
       HALF-UP (away from zero).
       Precision must be given by ``precision_digits`` or ``precision_rounding``,
       not both!

       :param float value: the value to round
       :param int precision_digits: number of fractional digits to round to.
       :param float precision_rounding: decimal number representing the minimum
           non-zero value at the desired precision (for example, 0.01 for a
           2-digit precision).
       :param rounding_method: the rounding method used: 'HALF-UP', 'UP' or 'DOWN',
           the first one rounding up to the closest number with the rule that
           number>=0.5 is rounded up to 1, the second always rounding up and the
           latest one always rounding down.
       :return: rounded float
    """
    rounding_factor = _float_check_precision(precision_digits=precision_digits,
                                             precision_rounding=precision_rounding)
    if rounding_factor == 0 or value == 0:
        return 0.0

    # NORMALIZE - ROUND - DENORMALIZE
    # In order to easily support rounding to arbitrary 'steps' (e.g. coin values),
    # we normalize the value before rounding it as an integer, and de-normalize
    # after rounding: e.g. float_round(1.3, precision_rounding=.5) == 1.5
    # Due to IEE754 float/double representation limits, the approximation of the
    # real value may be slightly below the tie limit, resulting in an error of
    # 1 unit in the last place (ulp) after rounding.
    # For example 2.675 == 2.6749999999999998.
    # To correct this, we add a very small epsilon value, scaled to the
    # the order of magnitude of the value, to tip the tie-break in the right
    # direction.
    # Credit: discussion with OpenERP community members on bug 882036

    normalized_value = value / rounding_factor # normalize
    sign = math.copysign(1.0, normalized_value)
    epsilon_magnitude = math.log(abs(normalized_value), 2)
    epsilon = 2**(epsilon_magnitude-52)

    # TIE-BREAKING: UP/DOWN (for ceiling[resp. flooring] operations)
    # When rounding the value up[resp. down], we instead subtract[resp. add] the epsilon value
    # as the the approximation of the real value may be slightly *above* the
    # tie limit, this would result in incorrectly rounding up[resp. down] to the next number
    # The math.ceil[resp. math.floor] operation is applied on the absolute value in order to
    # round "away from zero" and not "towards infinity", then the sign is
    # restored.

    if rounding_method == 'UP':
        normalized_value -= sign*epsilon
        rounded_value = math.ceil(abs(normalized_value)) * sign

    elif rounding_method == 'DOWN':
        normalized_value += sign*epsilon
        rounded_value = math.floor(abs(normalized_value)) * sign

    # TIE-BREAKING: HALF-UP (for normal rounding)
    # We want to apply HALF-UP tie-breaking rules, i.e. 0.5 rounds away from 0.
    else:
        normalized_value += math.copysign(epsilon, normalized_value)
        rounded_value = round(normalized_value)     # round to integer

    result = rounded_value * rounding_factor # de-normalize
    return result