from ipfml.filters import noise as nf


def get_noise_result(_image, _n, _noise_choice, _identical=False, _p=None):
    """Return image with applied noise using choice

    Args:
        image: image to convert
        _n: importance of noise expected [1, 999]
        _noise_choice: choise of noise filter to apply
        _identical: specify if the distribution is the same or not for each chanel
        _p: optional parameter for salt_pepper noise

    Returns:
        Noisy image with noise filter applied

    """

    noise_method = None
    function_name = _noise_choice + '_noise'

    try:
        noise_method = getattr(nf, function_name)
    except AttributeError:
        raise NotImplementedError("Noise filter `{}` not implement `{}`".format(nf.__name__, function_name))


    if _p:

        if _noise_choice != 'salt_pepper':
            raise ValueError("p parameter is only used for salt pepper noise...")

        return noise_method(_image, _n, identical=_identical, p=_p)
    else:
        return noise_method(_image, _n, identical=_identical)

