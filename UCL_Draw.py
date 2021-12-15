import random
import itertools
from collections import Counter


# DEFAULT VALUES

FIRST_PLACED_TEAMS = {
    "team_1": {"Team": "Man City", "Country": "England", "Group": "A"},
    "team_2": {"Team": "Liverpool", "Country": "England", "Group": "B"},
    "team_3": {"Team": "Ajax", "Country": "Netherlands", "Group": "C"},
    "team_4": {"Team": "Real Madrid", "Country": "Spain", "Group": "D"},
    "team_5": {"Team": "Bayern", "Country": "Germany", "Group": "E"},
    "team_6": {"Team": "Man United", "Country": "England", "Group": "F"},
    "team_7": {"Team": "LOSC", "Country": "France", "Group": "G"},
    "team_8": {"Team": "Juventus", "Country": "Italy", "Group": "H"},
}

SECOND_PLACED_TEAMS = {
    "team_1": {"Team": "PSG", "Country": "France", "Group": "A"},
    "team_2": {"Team": "Atletico Madrid", "Country": "Spain", "Group": "B"},
    "team_3": {"Team": "Sporting", "Country": "Portugal", "Group": "C"},
    "team_4": {"Team": "Inter", "Country": "Italy", "Group": "D"},
    "team_5": {"Team": "Benfica", "Country": "Portugal", "Group": "E"},
    "team_6": {"Team": "Villareal", "Country": "Spain", "Group": "F"},
    "team_7": {"Team": "Salzurg", "Country": "Austria", "Group": "G"},
    "team_8": {"Team": "Chelsea", "Country": "England", "Group": "H"},
}


# Main Function


def UCL_Draw(
    first_place_teams_dict=FIRST_PLACED_TEAMS,
    second_place_teams_dict=SECOND_PLACED_TEAMS,
):
    """
    This function simulates a UCL draw in the same way the draw is done in realty:
        - We select a random team for the "second placed" teams.
        - We compute a list of "first placed" available teams.
        - We randomly choose one of them.
        - Delete these two teams from the respective lists.

    Input:
        - first_placed_teams_dict : dictionary containing all the info about the "first placed" teams
        - second_placed_teams_dict : dictionary containing all the info about the "second placed" teams

        Information is:
            - Team Name
            - Team Country
            - Team Group

    Returns:
        - A list with all the draws

    Print:
        - Each drawn "second placed" team
        - Each avialbles teams
        - The selected "first placed" team
    """

    def _compatible_teams(
        first_placed_teams_list, target_second_team, second_placed_teams_list
    ):
        """
        This function, given a "second placed" team, returns the list of avaiable matches with
        "first placed team"

        Input:
            - first_placed_teams_list : list of all "first placed" teams left.
            - second_placed_teams_list : list of all "second placed" teams left (including the target team)
            - target_second_team : target "second_placed" team

        Returns:
            - filtered_teams_list : list of avaiable "first placed" team
        """

        def _remaining_draw(
            team, target_second_team, first_placed_teams_list, second_placed_teams_list
        ):
            """
            This function check if a possible "fist placed" team selection could create impossible draws
            for the remaining teams

            Input:
                - team : "first_placed" team selected
                - target_second_team : target "second_placed" team
                - first_placed_teams_list : list of all "first placed" teams left.
                - second_placed_teams_list : list of all "second placed" teams left (including the target team)

            Returns:
                - Boolean condition wrt the consistency of the choice
            """

            remaining_first_teams = first_placed_teams_list.copy()
            remaining_first_teams.remove(team)

            remaining_second_teams = second_placed_teams_list.copy()
            remaining_second_teams.remove(target_second_team)

            dict_available = {}
            for second_team in remaining_second_teams:

                target_country = second_place_teams_dict[second_team]["Country"]
                target_group = second_place_teams_dict[second_team]["Group"]

                available_teams = set(
                    [
                        team
                        for team in remaining_first_teams
                        if (
                            (first_place_teams_dict[team]["Country"] != target_country)
                            & (first_place_teams_dict[team]["Group"] != target_group)
                        )
                    ]
                )
                if len(available_teams) == 0:
                    return False

                dict_available[second_team] = available_teams

            for first in remaining_first_teams:
                union_set = set()
                for key, values in dict_available.items():
                    union_set = union_set.union(values)
                if first not in union_set:
                    return False

            list_avaiable_team = []
            for values in dict_available.values():
                list_values = [x for x in values]
                list_avaiable_team.append(list_values)

            for L in range(1, len(list_avaiable_team) + 1):
                for list_of_lists_available_team in itertools.combinations(
                    list_avaiable_team, L
                ):
                    set_available_team = set(
                        [x for z in list_of_lists_available_team for x in z]
                    )
                    if len(list_of_lists_available_team) > len(set_available_team):
                        return False

            return True

        ### start "_compatible_teams" function ###

        target_country = second_place_teams_dict[target_second_team]["Country"]
        target_group = second_place_teams_dict[target_second_team]["Group"]

        filtered_teams_list = [
            team
            for team in first_placed_teams_list
            if (
                (first_place_teams_dict[team]["Country"] != target_country)
                & (first_place_teams_dict[team]["Group"] != target_group)
                & (
                    _remaining_draw(
                        team,
                        target_second_team,
                        first_placed_teams_list,
                        second_placed_teams_list,
                    )
                    == True
                )
            )
        ]
        return filtered_teams_list

    ### start "UCL_Draw" function ###

    first_placed_teams_list = list(first_place_teams_dict.keys())
    second_placed_teams_list = list(second_place_teams_dict.keys())

    draws_list = []

    for _ in range(len(second_placed_teams_list)):

        target_second_team = random.choice(second_placed_teams_list)
        print(f"Extract : {second_place_teams_dict[target_second_team]['Team']}")

        available_first_teams = _compatible_teams(
            first_placed_teams_list, target_second_team, second_placed_teams_list
        )
        print(
            f"Available matching : {[first_place_teams_dict[team]['Team'] for team in available_first_teams]}"
        )

        target_first_team = random.choice(available_first_teams)
        print(
            f"Draw : {second_place_teams_dict[target_second_team]['Team']} vs {first_place_teams_dict[target_first_team]['Team']}"
        )

        first_placed_teams_list.remove(target_first_team)
        second_placed_teams_list.remove(target_second_team)

        draws_list.append(
            f"Draw : {second_place_teams_dict[target_second_team]['Team']} vs {first_place_teams_dict[target_first_team]['Team']}"
        )

        print("\n")

    return draws_list


if __name__ == "__main__":
    UCL_Draw()
