


# this class creates new unique non_terminal names --- why?
# removing left recursion always results in creation of new unique non_terminal symbols
# Let's have a set of computer generated names instead
class Name_generator():
    # non-static attributes:
    def __init__(self):
        self.segment_one = "CGLR-"  # segment one of the new Computer Generated Left Recursion (CGLR) name.
        self.current_index = 0    # This is the index of the current new name. It begins at zero by default

    def generate_new_name(self):
        new_name = self.segment_one + str(self.current_index)
        self.current_index = self.current_index + 1
        return new_name

# defining a global name_generator. So we can have only one set of names that are unique
name_generator = Name_generator()


# this function returns the name of the paragraph as a string
def get_paragraph_name(paragraph):
    return paragraph["token_value"]

# this function checks if a paragraph is infected with direct left recursion
# returns true if it has at least one DIRECT left recursion
def check_if_paragraph_has_direct_recursion(paragraph):
    paragraph_name = get_paragraph_name(paragraph)
    left_recursion_status = False

    # loop through the productions, check if any production begins with the paragraph name:
    for production in paragraph["productions"]:
        # if the first token is a terminal ... pass it
        if production[0]["token_type"] == "terminal":
            pass

        # if the first token is a non_terminal ... evaluate it
        if production[0]["token_type"] == "non_terminal":
            # if it has a different name from the paragraph name... pass it
            if production[0]["token_value"] != paragraph_name:
                pass
                
            # else, indicate the direct left_recursion_status... and exit loop
            elif production[0]["token_value"] == paragraph_name:
                left_recursion_status = True
                break
    return left_recursion_status



paragraph = {
            "token_value": "S",
            "productions": [
                [
                    {
                        "token_type": "non_terminal",
                        "token_value": "A"
                    },
                    {
                        "token_type": "terminal",
                        "token_value": "a"
                    }
                ],
                [
                    {
                        "token_type": "non_terminal",
                        "token_value": "B"
                    },
                    {
                        "token_type": "terminal",
                        "token_value": "b"
                    }
                ],
                [
                    {
                        "token_type": "terminal",
                        "token_value": "c"
                    }
                ],
                [
                    {
                        "token_type": "non_terminal",
                        "token_value": "A"
                    }
                ]
            ]
        }

status = check_if_paragraph_has_direct_recursion(paragraph)
print (status)
