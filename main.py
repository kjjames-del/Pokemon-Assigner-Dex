from dataclasses import dataclass
from drafter import *
import random

set_website_title(" Pokemon App ")
set_site_information(
    author="Kaiden James",
    description="Get a starter Pokémon or Play Who's That Pokémon and even search the Pokedex.",
    sources="Thanks to https://pokemondb.net/tools/text-list",
    planning=["_CS1 Final Project 1_ Design.pdf", "CS1 Final Project 0_ Pick a Problem.pdf"],
    links=["https://github.com/kjjames-del/Pokemon-Assigner-Dex"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Pokemon:
    pokedex_number: str
    name: str
    type_1: str
    type_2: str
    
@dataclass
class Pokedex:
    dex:list[Pokemon]
    random_pokemon: Pokemon

with open('pokemon.txt') as pokemon_file:
    file_list: list[Pokemon] = []
    for line in pokemon_file:
        split = line.strip().split(",")
        file_list.append(Pokemon(split[0],split[1],split[2],split[3]))
pokedex_list = Pokedex(file_list, "")
        
def find_pokemon(pokedex: Pokedex, inputed_pokedex_number: str) -> Pokemon:
    correct_pokedex_number = None
    for lines in pokedex.dex:
        if lines.pokedex_number == inputed_pokedex_number:
            correct_pokedex_number = lines
    if correct_pokedex_number == None:
        correct_pokedex_number = Pokemon("Not Found", "Not Found", "Not Found", "Not Found")         
    return correct_pokedex_number
        
def display_pokemon(pokemon: Pokemon)-> str:
    if pokemon.pokedex_number == "Not Found":
        return "This Pokemon doesn't exist"
    elif pokemon.type_2 != "":
        return "Pokedex Number: " + pokemon.pokedex_number + " " + "Name: " + pokemon.name + " " + "Type: " + pokemon.type_1 + "," + pokemon.type_2
    else:
        return "Pokedex Number: " + pokemon.pokedex_number + " " + "Name: " + pokemon.name + " " + "Type: " + pokemon.type_1 

def choose_starter(pokedex: Pokedex)-> Pokemon:
    return random.choice(pokedex.dex)

@route
def index(pokedex: Pokedex)-> Page:
    return Page(pokedex,
                [
                     Header("Pokemon App. Time To Be The Best There Ever Was"),
                     Button("Start", "name_page"),
                     Button("Play " + "Who's That Pokemon!", "guessing_game_page"),
                ],
            )


@route
def guessing_game_page(pokedex: Pokedex)-> Page:
    pokedex.random_pokemon = random.choice(pokedex.dex)
    if pokedex.random_pokemon.type_2 == "":
        description = ""
    else:
        description = ", " + pokedex.random_pokemon.type_2
    return Page(pokedex,
                [
                     Header("Who's That Pokemon!"),
                     Text("Pokedex Number: " + pokedex.random_pokemon.pokedex_number + " " + "Type: " + pokedex.random_pokemon.type_1 + description),
                     TextBox("inputed_name", " "),
                     Button("Ready", "answer_page"),
                ],
            )
@route
def answer_page(pokedex: Pokedex, inputed_name: str)-> Page:
    if pokedex.random_pokemon.name == inputed_name.strip().title():
        answer = "Correct"
    else:
        answer = "Sorry that's wrong"
    return Page(pokedex,
                [
                    Header(answer),
                    Text(pokedex.random_pokemon.name + " " + "vs " + inputed_name.strip().title()),
                    Button("Try Again ?", "guessing_game_page"),
                    Button("Exit", "index"),
                ],
            )


@route
def name_page(pokedex: Pokedex)-> Page:
    return Page(pokedex,
                [
                    Text("What's your name ?"),
                    TextBox("inputed_name", " "),
                    Button("Get starter", "starter_page"),
                ],
            )



@route
def starter_page(pokedex: Pokedex, inputed_name: str)-> Page:
    return Page(pokedex,
                [
                    Header("Congrats " + inputed_name + "."  + " " + "Your starter pokemon is " + choose_starter(pokedex).name + " " + " a perfect match."),
                    Button("Find a friends starter ? ", "friend_name_page"),
                    Button("Finished ? ", "index"),
                    Button("Search for a Pokemon ?", "search_page")
                ],
            )
                    

@route 
def friend_name_page(pokedex: Pokedex)-> Page:
    return Page(pokedex,
                [
                    Text("What's your friends name"),
                    TextBox("inputed_name", " "),
                    Button("Get friends starter", "starter_page"),
                ],
            )
    

@route 
def search_page(pokedex: Pokedex)-> Page:
    return Page(pokedex,
                [
                   Text("Type a pokedex number from 001 to 1025"),
                   TextBox("inputed_pokedex_number", ""),
                   Button("Continue", "pokemon_info_page")
                ],
            )

@route 
def pokemon_info_page(pokedex: Pokedex, inputed_pokedex_number: str)-> Page:
    return Page(pokedex,
                [
                   Header("You searched for" + " " + find_pokemon(pokedex, inputed_pokedex_number).name),
                   Text(display_pokemon(find_pokemon(pokedex, inputed_pokedex_number))),
                          Button("Return", "index"),
                          Button("Search Again", "search_page"),  
                ],
            )

start_server(pokedex_list)  

            
