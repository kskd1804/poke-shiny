class Offset:
    game_area_a_offset = 0x0000
    game_area_b_offset = 0xE000
    section_id_offset = 0x0FF4
    section_checksum_offset = 0x0FF6
    save_index_offset = 0x0FFC
    
    # Team list offsets
    team_size_offset = 0x234
    team_list_offset = 0x238

class Size:
    save_index_size = 4
    section_id_size = 2
    section_checksum_size = 2
    # Team list sizes
    team_size = 4

class Section:
    # Section count
    NUM_SECTIONS = 13
    SECTION_SIZE = 0x1000
    SECTION_DATA_SIZE = 3968

    # Section ID mapping
    TRAINER_INFO = 0
    TEAM_INFO = 1
    GAME_STATE = 2
    MISC_DATA = 3
    RIVAL_INFO = 4
    PC_BUFFER_A = 5
    PC_BUFFER_B = 6
    PC_BUFFER_C = 7
    PC_BUFFER_D = 8
    PC_BUFFER_E = 9
    PC_BUFFER_F = 10
    PC_BUFFER_G = 11
    PC_BUFFER_H = 12
    PC_BUFFER_I = 13

class PokemonConstants:
    pokemon_block_size = 0x64

    # offsets
    personality_value_offset = 0
    original_trainer_id_offset = 4
    nickname_offset = 8
    checksum_offset = 28
    data_offset = 32
    
    # sizes in bytes
    personality_value_size = 4
    original_trainer_id_size = 4
    nickname_size = 10
    checksum_size = 2
    data_size = 48
    subsection_block_size = 12

    # Pokemon Substructure order
    substructure_order = {
        0: ['G', 'A', 'E', 'M'],
        1: ['G', 'A', 'M', 'E'],
        2: ['G', 'E', 'A', 'M'],
        3: ['G', 'E', 'M', 'A'],
        4: ['G', 'M', 'A', 'E'],
        5: ['G', 'M', 'E', 'A'],
        6: ['A', 'G', 'E', 'M'],
        7: ['A', 'G', 'M', 'E'],
        8: ['A', 'E', 'G', 'M'],
        9: ['A', 'E', 'M', 'G'],
        10: ['A', 'M', 'G', 'E'],
        11: ['A', 'M', 'E', 'G'],
        12: ['E', 'G', 'A', 'M'],
        13: ['E', 'G', 'M', 'A'],
        14: ['E', 'A', 'G', 'M'],
        15: ['E', 'A', 'M', 'G'],
        16: ['E', 'M', 'G', 'A'],
        17: ['E', 'M', 'A', 'G'],
        18: ['M', 'G', 'A', 'E'],
        19: ['M', 'G', 'E', 'A'],
        20: ['M', 'A', 'G', 'E'],
        21: ['M', 'A', 'E', 'G'],
        22: ['M', 'E', 'G', 'A'],
        23: ['M', 'E', 'A', 'G'],
    }