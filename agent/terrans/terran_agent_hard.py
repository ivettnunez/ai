from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
import random
from absl import app


class TerranAgent(base_agent.BaseAgent):

    def __init__(self):
        super(TerranAgent, self).__init__()
        self.attack_coordinates = None
        self.upper_flag = False

    #Funcion to check if the input unit is selected
    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    #Function that returns a list with actual instances of the input unit
    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    #Function to check if the input action is available
    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    #Step function is where all of the decision making takes place
    def step(self, obs):
        super(TerranAgent, self).step(obs)

        #Check if it is the first step of the game
        if obs.first():
            #Get the centre x and y coordinates of our units on the minimap
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()

            #Set attack coordinates based on the position of our principal base
            #This information is also used to set as True or False a flag that will be needed to set more
            #accurate coordinates for constructions and attacks.
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)
                self.upper_flag = True
            else:
                self.attack_coordinates = (12, 16)
                self.upper_flag = False

        #Get actual total minerals
        mins = obs.observation.player.minerals

        #Attack if there are enough marines
        marines = self.get_units_by_type(obs, units.Terran.Marine)
        if len(marines) >= 25:
            if self.unit_type_is_selected(obs, units.Terran.Marine):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates)
            #Select marines army
            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")

        #Build Supply Depots (required to build Barracks)
        supply_depot = self.get_units_by_type(obs, units.Terran.SupplyDepot)
        if len(supply_depot) < 4 and mins >= 100:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                    if self.upper_flag:
                        #Check flag value to be more accurate with barracks coordinates construction
                        if len(supply_depot) == 0:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (73, 55))
                        elif len(supply_depot) == 1:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (80, 55))
                        elif len(supply_depot) == 2:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (73, 65))
                        elif len(supply_depot) == 3:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (80, 65))
                    else:
                        if len(supply_depot) == 0:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (3, 55))
                        elif len(supply_depot) == 1:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (10, 55))
                        elif len(supply_depot) == 2:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (3, 65))
                        elif len(supply_depot) == 3:
                            return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (10, 65))

            #Select scvs
            scvs = self.get_units_by_type(obs, units.Terran.SCV)
            if len(scvs) > 0:
                scv = random.choice(scvs)
                return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))


        #Build barracks (required to train marines)
        barracks = self.get_units_by_type(obs, units.Terran.Barracks)
        if len(barracks) < 4 and mins > 150:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                    #Check flag value to be more accurate with barracks coordinates construction
                    if self.upper_flag:
                        if len(barracks) == 0:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (80, 10))
                        elif len(barracks) == 1:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (80, 20))
                        elif len(barracks) == 2:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (80, 30))
                        elif len(barracks) == 3:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (80, 40))

                    else:
                        if len(barracks) == 0:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (10, 10))
                        elif len(barracks) == 1:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (10, 20))
                        elif len(barracks) == 2:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (10, 30))
                        elif len(barracks) == 3:
                            return actions.FUNCTIONS.Build_Barracks_screen("now", (10, 40))

            #Select scvs
            scvs = self.get_units_by_type(obs, units.Terran.SCV)
            if len(scvs) > 0:
                scv = random.choice(scvs)
                return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))


        #Build Refineries
        '''ref = self.get_units_by_type(obs, units.Terran.Refinery)
        if len(ref) < 1:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_Refinery_screen("now", (x, y))'''

        #Train marines when there are enough barracks
        if len(barracks) == 4:
            if self.unit_type_is_selected(obs, units.Terran.Barracks):
                marines = self.get_units_by_type(obs, units.Terran.Marine)
                if len(marines) < 25 and mins >=50:
                    if self.can_do(obs, actions.FUNCTIONS.Train_Marine_quick.id):
                        return actions.FUNCTIONS.Train_Marine_quick("now")
            b = random.choice(barracks)
            if b.x <= 83 and b.y <=83 and b.x > 0 and b.y > 0:
                return actions.FUNCTIONS.select_point("select_all_type", (b.x, b.y))

        #Train scvs when there are lees than 12. If there are 12 or more, select them.
        scvs = self.get_units_by_type(obs, units.Terran.SCV)
        if len(scvs) > 0:
            if len(scvs) < 12 and mins >= 50:
                if self.unit_type_is_selected(obs, units.Terran.CommandCenter):
                    if self.can_do(obs, actions.FUNCTIONS.Train_SCV_quick.id):
                        return actions.FUNCTIONS.Train_SCV_quick("now")

                command_center = self.get_units_by_type(obs, units.Terran.CommandCenter)
                comcent = random.choice(command_center)
                if comcent.x <= 83 and comcent.y <=83 and comcent.x > 0 and comcent.y > 0:
                    return actions.FUNCTIONS.select_point("select_all_type", (comcent.x, comcent.y))
            scv = random.choice(scvs)
            if scv.x <= 83 and scv.y <=83 and scv.x > 0 and scv.y > 0:
                return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

        return actions.FUNCTIONS.no_op()


def main(unused_argv):
    agent = TerranAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name ="Simple128",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.hard)],
                agent_interface_format = features.AgentInterfaceFormat(
                    feature_dimensions = features.Dimensions(screen=84, minimap=64),
                    use_feature_units = True
                ),
                step_mul = 14,
                game_steps_per_episode = 0, #length of each game, 0 for run as long as necessary
                visualize=True
            ) as env:

                agent.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent.reset()

                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app.run(main)
