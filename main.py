from PokeSave import PokeSave

poke = PokeSave(file_path="7th_sav_female_k_with_3_poke.sav")
poke.make_shiny()
poke.save_file("test_3.sav")