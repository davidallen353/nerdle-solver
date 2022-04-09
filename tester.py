import nerdle_solver as nerd
from copy import deepcopy

good_char_input = "        " # = st.text_input("Green characters (space separated):")
while len(good_char_input) < 8:
    good_char_input += " "
print(len(good_char_input))
_known_chars = [_char.strip() for _char in good_char_input if _char != ""]

bad_char_input = "1+429"# = st.text_input("Black characters:")
_bad_chars = [_char for _char in bad_char_input if _char != ""]

p1 = "" #= st.text_input("Purple in Box 1:")
p2 = "" #= st.text_input("Purple in Box 2:")
p3 = "" #= st.text_input("Purple in Box 3:")
p4 = "*" #= st.text_input("Purple in Box 4:")
p5 = "7" #= st.text_input("Purple in Box 5:")
p6 = "=" #= st.text_input("Purple in Box 6:")
p7 = "" #= st.text_input("Purple in Box 7:")
p8 = "" #= st.text_input("Purple in Box 8:")

_good_chars = list(p1) + list(p2) + list(p3) + list(p4) + list(p5) + list(p6) + list(p7) + list(p8)
_known_bad_chars = deepcopy(nerd.DEFAULT_KNOWN_BAD_CHAR)

_known_bad_chars[0] += list(p1)
_known_bad_chars[1] += list(p2)
_known_bad_chars[2] += list(p3)
_known_bad_chars[3] += list(p4)
_known_bad_chars[4] += list(p5)
_known_bad_chars[5] += list(p6)
_known_bad_chars[6] += list(p7)
_known_bad_chars[7] += list(p8)

char_list = nerd.build_character_list(_bad_chars)
print(char_list)
guesses = nerd.generate_guesses(char_list, _known_chars, _good_chars, _known_bad_chars)
print(guesses)

print(nerd.make_recommendation(guesses,_good_chars))