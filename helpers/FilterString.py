def format_filter_string(filter_string):
    """
    This function takes a filter string and replaces certain characters and substrings.
    """
    # Perform the replacements
    filter_string = filter_string.replace("'", '"') \
                                 .replace("\\", "\\\\") \
                                 .replace('"', '\\"') \
                                 .replace("-eq", "eq") \
                                 .replace("-ne", "ne") \
                                 .replace("-sw", "sw") \
                                 .replace("-gt", "gt") \
                                 .replace("-lt", "lt")
    return filter_string

# Example usage
if __name__ == "__main__":
    original_filter = "example-filter-string -eq 'value'"
    formatted_filter = format_filter_string(original_filter)
    print(f"Original Filter: {original_filter}")
    print(f"Formatted Filter: {formatted_filter}")