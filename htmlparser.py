def first_element_with_tag(element_list, tag_name):
    """
    Returns the first element in an element list with the tag name specified.
    :param element_list: List to search.
    :param tag_name: Tag to extract.
    :return: First element with tag name. None if not found.
    """
    return next((x for x in element_list if x.tag == tag_name), None)


def first_element_with_tag_and_attributes(element_list, tag_name, attribute_name, attribute_value):
    """
    Returns the first element in an element list with the tag name specified.
    :param element_list: List to search.
    :param tag_name: Tag to extract.
    :param attribute_name: Attribute to find on tag.
    :param attribute_value: Value of attribute.
    :return: First element with tag and attributes that match. None if not found.
    """
    return next((x for x in element_list if (x.tag == tag_name) and
                 (x.attrib.get(attribute_name) == attribute_value)), None)


def all_elements_with_tag_and_attributes(element_list, tag_name, attribute_name, attribute_value):
    """
    Returns all elements in an element list with the tag name specified.
    :param element_list: List to search.
    :param tag_name: Tag to extract.
    :param attribute_name: Attribute to find on tag.
    :param attribute_value: Value of attribute.
    :return: All elements that match tag and attribute values. None if not found.
    """
    return [x for x in element_list if (x.tag == tag_name) and (x.attrib.get(attribute_name) == attribute_value)]


def strip_time_zone(timezone_string):
    """
    Strips the timezone from a Facebook date string.
    :param timezone_string: String to strip timezone from.
    :return: String without timezone.
    """
    if timezone_string[-3:] == "UTC":
        return timezone_string[:-4]
    return timezone_string[:-7]