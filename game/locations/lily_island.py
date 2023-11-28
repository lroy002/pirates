from game import location 
#there is some pretence that the game might not be played over the term 
#so we use a custom function announce to print things instead of print 
from game.display import announce 
import random 
import game.config as config 
import game.items as items 
from game.events import *
import game.combat as combat 

class DemoIsland(location.Location):
    def __init__ (self, x, y, world):
        super().__init__(x,y,world)
        #object orientted handling. Super() refers to the parent class
        #location in this case
        #so this runs the initializer of location 
        self.name = "island"
        self.symbol = "I" #symbol for map
        self.visitable = True #marks the island as a place the pirates can go ashore 
        self.locations = {} #dictionary of sub-locations on the island 
        self.locations["beach"] = Beach(self)
        self.locations["forest"] = Forest(self)
        self.locations["swamp"] = Swamp(self)
        self.locations["flowers"] = Flowers(self)
        self.locations["shipwreck"] = Shipwreck(self)
        self.starting_location = self.locations["beach"]
        
        
    def enter(self, ship):
        #what to do when the ship visits this loc on the map
        announce("arrived at an island")
            
        
    #bolierplate for starting visit    
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        
        
#Sub-locations (Beach, Swamp, Forest, Flowers, Shipwreck)

#START OF BEACH HERE 
class Beach(location.SubLocation):
    def __init__ (self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        #the verb dict was set up by super() __init__
        #"go north" has handling that causes sublocations to 
        #just get the directions.
        self.verbs["north"] = self 
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self 
        self.verbs["west"] = self 
        self.events_chance = 50
        #self.events.append(seagull.Seagull())
        #self.events.append(drowned_pirates.Drowned_Pirates())
    def enter(self):
        announce ("You arrived at the peaceful pink sand beach. Your ship is at anchor in a small bay to the south.")
    #one of the core functions. Contains handeling for everything that the player can do here 
    #more complex actions should have dedicated functions to handle them.
    
    
    def process_verb(self, verb, cmd_list, nouns):
    #one of the core functions. Contains handeling for everything that the player can do here 
    #more complex actions should have dedicated functions to handle them.
        if (verb == "south"):
            announce("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            announce("You walk twords the forest, and come to a swamp.")
            config.the_player.next_loc = self.main_location.locations["swamp"]
        if (verb == "north"):
            announce("You walk out of the swamp and into the forest.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "east"):
            announce("You walk the way around the island on eastern side. You arrive at a patch of tropical flowers.")
            config.the_player.next_loc = self.main_location.locations["flowers"]
        if (verb == "west"):
            announce("You walk the way around the island on the western side. You arrive at a shipwreck.")
            config.the_player.next_loc = self.main_location.locations["shipwreck"]

      
                
#START OF SWAMP HERE 
class Swamp(location.SubLocation):
    def __init__ (self, main_location):
        super().__init__(main_location)
        self.name = "swamp"
        #the verb dict was set up by super() __init__
        #"go north" has handling that causes sublocations to 
        #just get the directions.
        self.verbs["north"] = self 
        self.verbs["north"] = self
        self.verbs["south"] = self 
        self.verbs["east"] = self 
        self.verbs["west"] = self 
        self.events_chance = 50
        #self.events.append(seagull.Seagull())
        #self.events.append(drowned_pirates.Drowned_Pirates())
        self.verbs["take"] = self
        self.item_in_forest = Saber()
        self.item_in_clothes = items.Flintlock()
        self.event_chance = 50
        #self.events.append(Panther())
        #self.events.append(drowned_pirates.DrownedPirates())
        
    
    def enter (self):
        announce("You walk into the islands swamp.")
        if self.item_in_forest != None:
            description = description + "you see a " + self.item_in_tree.name + " stuck in the mud"
        if self.item_in_clothes != None:
            description = description + "you see a " + self.item_in_clothes.name + " sticking out of the mud infront of you."
        announce(description)
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            announce("You walk twords the forest, and come to a swamp.")
            config.the_player.next_loc = self.main_location.locations["swamp"]
        if (verb == "north"):
            announce("You walk out of the swamp and into the forest.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "east"):
            announce("You walk the way around the island on eastern side. You arrive at a patch of tropical flowers.")
            config.the_player.next_loc = self.main_location.locations["flowers"]
        if (verb == "west"):
            announce("You walk the way around the island on the western side. You arrive at a shipwreck.")
            config.the_player.next_loc = self.main_location.locations["shipwreck"]
        
        #if(verb in ["north", "south", "east", "west"]):
            #config.the_player.next_loc = self.main_loation.locations["swamp"]
        if(verb == "take"):
            #The player will type something like "take saber" or "take all"
            if(self.item_in_swamp == None and self.item_in_clothes == None):
                announce("You don't see anything to take.")
            #they just typed "take"    
            elif(len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False
                i = self.item_in_swamp
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " +i.name)
                    config.the_player.add_to_inventory(i)
                    self.item_in_swamp = None
                    config.the_player_go = True 
                    at_least_one = True
                at_least_one = False 
                i = self.item_in_swamp
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " +i.name + "out of the pile... looks like something was eaten here")
                    config.the_player.add_to_inventory(i)
                    self.item_in_swamp = None
                    config.the_player_go = True 
                    at_least_one = True
                if not at_least_one:
                    #perhaps the player types "take Apple"
                    announce("you don't see one of those around")
                
                
                      
                
#START OF FOREST HERE    
class Forest(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "forest"
        self.verbs["north"] = self 
        self.verbs["south"] = self 
        self.verbs["east"] = self 
        self.verbs["west"] = self 
        
        #Add some treasure! 
        self.verbs["take"] = self
        self.item_in_forest = Saber()
        self.item_in_clothes = items.Flintlock()
        self.event_chance = 50
        #self.events.append(man_eating_monkey.ManEatingMonkeys())
        #self.events.append(drowned_pirates.DrownedPirates())
        
    def enter (self):
        announce("You arrive at the serene forest on the island.")
        #if self.item_in_forest != None:
            #description = description + "you see a " + self.item_in_tree.name + " stuck in a tree"
        #if self.item_in_clothes != None:
            #description = description + "you see a " + self.item_in_clothes.name + " in a pile of shreaded clothes on the forest floor"
        #announce(description)
        
    def process_verb(self, verb, cmd_list, nouns):
        #if(verb in ["north", "south", "east", "west"]):
            #config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "south"):
            announce("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            announce("You walk twords the forest, and come to a swamp.")
            config.the_player.next_loc = self.main_location.locations["swamp"]
        if (verb == "north"):
            announce("You walk out of the swamp and into the forest.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "east"):
            announce("You walk the way around the island on eastern side. You arrive at a patch of tropical flowers.")
            config.the_player.next_loc = self.main_location.locations["flowers"]
        if (verb == "west"):
            announce("You walk the way around the island on the western side. You arrive at a shipwreck.")
            config.the_player.next_loc = self.main_location.locations["shipwreck"]
        if(verb == "take"):
            #The player will type something like "take saber" or "take all"
            if(self.item_in_forest == None and self.item_in_clothes == None):
                announce("You don't see anything to take.")
            #they just typed "take"    
            elif(len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False
                i = self.item_in_forest
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " +i.name)
                    config.the_player.add_to_inventory(i)
                    self.item_in_forest = None
                    config.the_player_go = True 
                    at_least_one = True
                at_least_one = False 
                i = self.item_in_forest
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " +i.name + "out of the pile... looks like something was eaten here")
                    config.the_player.add_to_inventory(i)
                    self.item_in_forest = None
                    config.the_player_go = True 
                    at_least_one = True
                if not at_least_one:
                    #perhaps the player types "take Apple"
                    announce("you don't see one of those around")
                    
#START OF FLOWERS HERE    
class Flowers (location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "flowers"
        self.verbs["north"] = self 
        self.verbs["north"] = self
        self.verbs["south"] = self 
        self.verbs["east"] = self 
        self.verbs["west"] = self 
        
        #Add some treasure! 
        self.verbs["take"] = self
        self.item_in_forest = Saber()
        self.item_in_clothes = items.Flintlock()
        self.event_chance = 50
        #self.events.append(man_eating_monkey.ManEatingMonkeys())
        #self.events.append(drowned_pirates.DrownedPirates())
        
    def enter (self):
        announce("You walk into the beautiful patch of tropical flowers.")
        #if self.item_in_forest != None:
            #description = description + "you see a " + self.item_in_tree.name + " stuck in a tree"
        #if self.item_in_clothes != None:
            #description = description + "you see a " + self.item_in_clothes.name + " in a pile of shreaded clothes on the forest floor"
        #announce(description)
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            announce("You walk twords the forest, and come to a swamp.")
            config.the_player.next_loc = self.main_location.locations["swamp"]
        if (verb == "north"):
            announce("You walk out of the swamp and into the forest.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "east"):
            announce("You walk the way around the island on eastern side. You arrive at a patch of tropical flowers.")
            config.the_player.next_loc = self.main_location.locations["flowers"]
        if (verb == "west"):
            announce("You walk the way around the island on the western side. You arrive at a shipwreck.")
            config.the_player.next_loc = self.main_location.locations["shipwreck"]
        #if(verb in ["north", "south", "east", "west"]):
            #config.the_player.next_loc = self.main_location.locations["flowers"]
#my puzzle will be here!


#START OF Shipwreck HERE    
class Shipwreck (location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Shipwreck"
        self.verbs["north"] = self 
        self.verbs["north"] = self
        self.verbs["south"] = self 
        self.verbs["east"] = self 
        self.verbs["west"] = self 
        
        #Add some treasure! 
        self.verbs["take"] = self
        self.item_in_forest = Saber()
        self.item_in_clothes = items.Flintlock()
        self.event_chance = 50
        #self.events.append(man_eating_monkey.ManEatingMonkeys())
        #self.events.append(drowned_pirates.DrownedPirates())
        
    def enter (self):
        announce("You walk closer to the shipwreck.")     
             
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            announce("You walk twords the forest, and come to a swamp.")
            config.the_player.next_loc = self.main_location.locations["swamp"]
        if (verb == "north"):
            announce("You walk out of the swamp and into the forest.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "east"):
            announce("You walk the way around the island on eastern side. You arrive at a patch of tropical flowers.")
            config.the_player.next_loc = self.main_location.locations["flowers"]
        if (verb == "west"):
            announce("You walk the way around the island on the western side. You arrive at a shipwreck.")
            config.the_player.next_loc = self.main_location.locations["shipwreck"]         
            

class Saber(items.Item):
    def __init__(self):
        super().__init__("saber", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"
        
#class Macaque(combat.Monster):
    #def __init__ (self, name):
        #attacks = {}
        #attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        #super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))
        
        
#class Panther:
    #def __init__(self):
        #self.name = Panther 
        #attacks = {}
        #attacks ["bite"] = ["bites", random.randrange(70, 101), (10,20)]
        #super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))
        
    #def process (self, world):
        #result = {}
        #result["message"] = "the panthers are defeated!"
        #n_appearing = random.randint(4, 7) 
        #monsters = []  
        #n = 1
        #while n <= n_appearing:
            #monsters.append(Panther("Deadly panther " + str(n)))  
            #n += 1
        #announce("The crew is attacked by wild panthers!") 
        #combat_result = self.combat(monsters)
        #if random.randrange(2) == 0:
            #result["newevents"] = [self]
        #else:
            #result["newevents"] = []
        #config.the_player.ship.food += n_appearing * 3

        #return result
        
        