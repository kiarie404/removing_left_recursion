


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

# this function takes in an DIRECt recursion infected paragraph
# it returns clean paragraph(s) that dont have Recursion
# those new paragraphs get returned in an array
def generate_new_paragraphs_after_removing_direct_recursion(infected_paragraph):

    infected_paragraph_name = get_paragraph_name(infected_paragraph)

    # create two new empty paragrapghs
    paragraph_root = {}
    paragraph_child = {}

    # let paragraph root have the same name as the infected_paragraph
    paragraph_root["token_value"] = infected_paragraph_name
    paragraph_root["productions"] = []

    # let paragraph_child have a new unique name :
    new_non_terminal_token = {"token_type" : "non_terminal", "token_value" : name_generator.generate_new_name() }
    paragraph_child["token_value"] = new_non_terminal_token["token_value"]
    paragraph_child["productions"] = []

    # loop through the productions of the infected paragraph
    for production in infected_paragraph["productions"]:
        # if a production begins with a terminal and that terminal is not LAMBDA...
        if (production[0]["token_type"] == "terminal") and (production[0]["token_value"] != "LAMBDA"):
            new_production = [] # create a new empty priduction.
            new_production = production # copy the contents of production into it
            new_production.append(new_non_terminal_token) # append the new_non_terminal_token at the productions end
            paragraph_root["productions"].append(new_production) # add the newly formed production to the new paragraph_root

        # if a production has a LAMBDA only...
        elif (production[0]["token_type"] == "terminal") and (production[0]["token_value"] == "LAMBDA") and (len(production) == 1):
            new_production = [] # create a new empty priduction.
            new_production.append(new_non_terminal_token) # append the new_non_terminal_token at the productions end
            paragraph_root["productions"].append(new_production) # add the newly formed production to the new paragraph_root

        # if production is an un-offensive non_terminal...
        elif (production[0]["token_type"] == "non_terminal") and (production[0]["token_value"] != infected_paragraph_name):
            new_production = [] # create a new empty priduction.
            new_production = production # copy the contents of production into it
            new_production.append(new_non_terminal_token) # append the new_non_terminal_token at the productions end
            paragraph_root["productions"].append(new_production) # add the newly formed production to the new paragraph_root

        # if production has offensive non_terminal
        elif (production[0]["token_type"] == "non_terminal") and (production[0]["token_value"] == infected_paragraph_name):
            production_with_backlog_tokens_only = production[1:] # slice off the first offensive token
            new_production = production_with_backlog_tokens_only
            new_production.append(new_non_terminal_token) # append the new_non_terminal_token at the productions end
            paragraph_child["productions"].append(new_production) # add the newly formed production to the new paragraph_root


    # after the loop, insert a lambda production to the paragraph_child
    LAMBDA_token = {"token_type" : "terminal", "token_value" : "LAMBDA"}
    new_production = [LAMBDA_token]
    paragraph_child["productions"].append(new_production)

    array_of_cleans = [] # create an array of clean paragraphs
    # strore paragraphs that have at least one production
    if ( len(paragraph_root["productions"]) >= 1):
        array_of_cleans.append(paragraph_root)
    if ( len(paragraph_child["productions"]) >= 1):
        array_of_cleans.append(paragraph_child)

    return array_of_cleans

# this function displays a paragraph contents
def display(paragraph):
    print ("\n---- ", paragraph["token_value"], " -----")
    for production in paragraph["productions"]:
        print(production)

paragraph = {
            "token_value": "S",
            "productions": [
                [
                    {
                        "token_type": "non_terminal",
                        "token_value": "S"
                    },
                    {
                        "token_type": "terminal",
                        "token_value": "a"
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
                        "token_value": "S"
                    },
                    {
                        "token_type": "terminal",
                        "token_value": "a"
                    }
                ],
                [
                    {
                        "token_type": "terminal",
                        "token_value": "d"
                    }
                ]
            ]
        }
status = check_if_paragraph_has_direct_recursion(paragraph)
arr = generate_new_paragraphs_after_removing_direct_recursion(paragraph)
for element in arr:
    display(element)
