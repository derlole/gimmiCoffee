
# this function is processing the cyclic data from the esp format:
#                           [off_value/on_value]
# {
#   # eingänge
#   "an":                   [1/0],
#   "bereit":               [1/0],
#   "fehler":               [1/0],
#   "bohnen_voll":          [1/0],
#   "Wasser_voll":          [1/0],
#
#   # ausgänge
#   "einschalten":          [0/1],
#   "starten":              [0/1],
#   
#   # status
#   "kaffee_machen":        [0/1],
#   "vorbereitung":         [0/1],
#   "kaffee_fertig":        [0/1],
# }

def refactor_and_use_esp_data(data):
    return
