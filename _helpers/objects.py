def partial_flat(obj, subobj):
    """
    Returns the initial object with subobj flattened within it.
    Merges the attributes of a sub-object (subobj) into the parent object (obj).

    :param obj: The object to be flattened.
    :param subobj: The name of the attribute of obj that needs to be flattened into obj.
    """
    try:
        # Cas où obj est un dictionnaire
        if hasattr(obj, '__getitem__'):
            obj.update(obj[subobj])

        # Cas où obj est un objet, mais subobj est un dictionnaire
        elif hasattr(obj, subobj) and isinstance(getattr(obj, subobj), dict):
            obj.__dict__.update(getattr(obj, subobj))

    except KeyError:
        print(f"Le sous-objet '{subobj}' n'existe pas dans l'objet donné.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'aplatissement : {e}")

    return obj
