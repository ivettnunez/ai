
from pysc2.agents import base_agent
from pysc2.env import sc2_env #used to spacify players(race), game difficulty
from pysc2.lib import actions, features, units #pysc2/lib/features.py
from absl import app
import random

class ZergAgent(base_agent.BaseAgent):

    def __init__(self):
        super(ZergAgent, self).__init__()
        self.attack_coordinates = None

    #function to check sinle and multi seletions to see if the first selected unit is the correct type
    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    #step method is where all of our decision making take place
    def step(self, obs):
        super(ZergAgent, self).step(obs) #herencia de BaseAgent super(subclass, instance of subclass). ****Si no especificas más funciones, ¿sólo hereda esta?

        if obs.first(): #checks if it is the first step of the game
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()

            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)
            else:
                self.attack_coordinates = (12, 16)
        zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
        if len(zerglings) >= 10:
            if self.unit_type_is_selected(obs, units.Zerg.Zergling):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates)

            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")

        #get the list of spawing pools
        spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
        if len(spawning_pools) == 0:
            if self.unit_type_is_selected(obs, units.Zerg.Drone):
                #check to have enough minerals to build
                if self.can_do(obs, actions.FUNCTIONS.Build_SpawningPool_screen.id):
                    #build the Spawning Pool
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)

                    return actions.FUNCTIONS.Build_SpawningPool_screen("now", (x, y))


            #get the list of drones. Recorrer y guardar unit si es de tipo Zerg.Drone
            drones = self.get_units_by_type(obs, units.Zerg.Drone)
            if len(drones) > 0:
                drone = random.choice(drones)

                return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

        if self.unit_type_is_selected(obs, units.Zerg.Larva):

            free_supply = (obs.observation.player.food_cap - obs.observation.player.food_used)
            if free_supply == 0:
                if self.can_do(obs, actions.FUNCTIONS.Train_Overlord_quick.id):
                    return actions.FUNCTIONS.Train_Overlord_quick("now")

            if self.can_do(obs, actions.FUNCTIONS.Train_Zergling_quick.id): #(actions.FUNCTIONS.Train_Zergling_quick.id in obs.observation.available_actions):
                return actions.FUNCTIONS.Train_Zergling_quick("now")

        larvae = self.get_units_by_type(obs, units.Zerg.Larva)
        if len(larvae) > 0:
             larva = random.choice(larvae)

             return actions.FUNCTIONS.select_point("select_all_type", (larva.x, larva.y))



        return actions.FUNCTIONS.no_op()

def main(unused_argv):
    agent = ZergAgent()
    try:
        while True: #siempre vuelve a iniciar el juego
            with sc2_env.SC2Env(
                map_name="Simple64",
                players = [
                    sc2_env.Agent(sc2_env.Race.zerg), #first player
                    sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.very_easy) #second player is a bot
                ],
                agent_interface_format = features.AgentInterfaceFormat(
                    feature_dimensions = features.Dimensions(screen=84, minimap=64), #determine how many pixels of data are in each feature layer***
                    use_feature_units = True
                ),
                step_mul = 16, #hoy many game steps pass before the bot choose an action to take****
                game_steps_per_episode = 0, #length of each game, 0 for run as long as necessary
                visualize = True #to see details about observations layers available to the bot
            ) as env:

                agent.setup(env.observation_spec(), env.action_spec()) #funcion de la libreria importada como base_agent

                timesteps = env.reset() #funcion importada como sc2_env. timespets tiene las observaciones, que es toda la informacion que describe al ambiente
                agent.reset()

                while True: #todo el tiempo envia las observaciones
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)


    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    app.run(main)
