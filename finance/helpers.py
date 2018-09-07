def flatten_form_data(form_data):
    all_form_data = []
    for name, value in form_data.items():
        if isinstance(value, (list, tuple)):
            all_form_data += [(name, item) for item in value]
        else:
            all_form_data.append((name, value))
    return all_form_data
