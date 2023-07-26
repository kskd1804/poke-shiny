from constants import Offset, Size, Section, PokemonConstants
from Pokemon import Pokemon

class PokeSave:    

    def __init__(self, file_path):
        self.file_path = file_path
    
    def open(self):
        try:
            file = open(self.file_path, "rb")
            self.contents = file.read()
            file.close()
        except OSError as e:
            print(f"Unable to open {self.file_path}: {e}", file=sys.stderr)
            return

    def make_shiny(self):
        self.open()
        self.game_area_offset = self.get_latest_game_area_offset()
        self.team_info_section_offset = self.get_section_offset(Section.TEAM_INFO)
        team_size = self.get_team_size()
        print("Total pokemons found: ", team_size)
        for poke_index in range(team_size):
            pokemon = Pokemon(self.read(self.team_info_section_offset + Offset.team_list_offset + (poke_index * PokemonConstants.pokemon_block_size), PokemonConstants.pokemon_block_size))
            pokemon.crypt_data()
            pokemon.set_personality_value()
            pokemon.crypt_data()
            self.overwrite(self.team_info_section_offset + Offset.team_list_offset + (poke_index * PokemonConstants.pokemon_block_size), PokemonConstants.pokemon_block_size, pokemon.get_contents())
            print(f"Processed pokemon {poke_index + 1}")
        checksum = self.calculate_checksum(self.read(self.team_info_section_offset, Section.SECTION_DATA_SIZE))
        self.overwrite(self.team_info_section_offset + Offset.section_checksum_offset, Size.section_checksum_size, checksum.to_bytes(2, byteorder='little'))
    
    def calculate_checksum(self, data):
        checksum = 0x0
        for i in range(0, len(data), 4):
            checksum += int.from_bytes(data[i:i+4], byteorder='little')
        upper_checksum = (checksum >> 16) & 0xFFFF
        lower_checksum = checksum & 0xFFFF
        final_checksum = upper_checksum + lower_checksum
        final_checksum = final_checksum & 0xFFFF
        return final_checksum  

    def read(self, address, num_bytes):
        start = address - 0x0000
        end = start + num_bytes
        return self.contents[start:end]

    def overwrite(self, address, num_bytes, new_bytes):
        start = address - 0x0000
        end = start + num_bytes
        self.contents = self.contents[:start] + new_bytes + self.contents[end:]

    def get_latest_game_area_offset(self):
        save_index_a_hex = self.read(address=Offset.game_area_a_offset + Offset.save_index_offset, num_bytes=Size.save_index_size)        
        save_index_a = int.from_bytes(save_index_a_hex, byteorder='little')
        save_index_a = save_index_a if save_index_a != 4294967295 else 0
        save_index_b_hex = self.read(address=Offset.game_area_b_offset + Offset.save_index_offset, num_bytes=Size.save_index_size)
        save_index_b = int.from_bytes(save_index_b_hex, byteorder='little')
        save_index_b = save_index_b if save_index_b != 4294967295 else 0
        return Offset.game_area_a_offset if save_index_a > save_index_b else Offset.game_area_b_offset

    def get_section_offset(self, section_id):
        first_section_id = self.read(address=self.game_area_offset + Offset.section_id_offset, num_bytes=Size.section_id_size)
        first_section_id = int.from_bytes(first_section_id, byteorder='little')
        num_section_gap = (Section.NUM_SECTIONS - first_section_id + section_id + 1) % Section.NUM_SECTIONS
        return self.game_area_offset + (num_section_gap * Section.SECTION_SIZE)

    def get_team_size(self):
        return int.from_bytes(self.read(self.team_info_section_offset + Offset.team_size_offset, Size.team_size), byteorder='little')
        

    def save_file(self, file_path="PokeShiny.sav"):
        try:
            f = open(file_path, 'wb')
            f.write(self.contents)
            f.close()
        except OSError as e:
            print(f"Unable to write {self.file_path}: {e}", file=sys.stderr)
            return