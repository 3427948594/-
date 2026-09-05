# 黑油矿井机
from dataclasses import dataclass, asdict
import math

def clamp(x, a, b):
    return max(a, min(b, x))

class FacelessOilPress:
    def __init__(self,
                 fear_capacity=1e6,
                 stagnation_cap=200.0,
                 life_weight=0.9,
                 fear_weight=8.0):
        self.machine_state = "Sitting in Hell"
        self.fear_value = 0.0  # fuel / accumulated fear
        self.black_mani_beads = {"pure_desire": 0.0, "pollution_obsession": 0.0}
        self.stagnation_level = 0.0  # Measures how stuck the machine is
        # parameters
        self.fear_capacity = fear_capacity
        self.stagnation_cap = stagnation_cap
        self.life_weight = life_weight
        self.fear_weight = fear_weight

    def log(self, msg):
        print(msg)

    def devour_living_beings(self, living_being):
        """Refine a being into fear_value and bead fragments. Returns a dict result."""
        self.log(f"The faceless one looks down; a {living_being.type} is offered to the press.")
        # compute extracted fear/oil with configurable weights and soft cap
        extracted_oil = living_being.life_essence * self.life_weight + living_being.fear * self.fear_weight
        # soft cap on contribution
        extracted_oil = clamp(extracted_oil, 0.0, 1e5)
        prev_fear = self.fear_value
        self.fear_value = clamp(self.fear_value + extracted_oil, 0.0, self.fear_capacity)

        if living_being.has_glimmer_of_light:
            self.black_mani_beads["pure_desire"] += 0.1
            # light slightly reduces stagnation (but bounded)
            self.stagnation_level = clamp(self.stagnation_level - 0.5, 0.0, self.stagnation_cap)
            self.log("A faint light flickers, momentarily disturbing the eternal stagnation.")
            effect = "light_reduced"
        else:
            self.black_mani_beads["pollution_obsession"] += 1.0
            self.stagnation_level = clamp(self.stagnation_level + 2.0, 0.0, self.stagnation_cap)
            self.log("The darkness sinks deeper, stagnation tightens its grip.")
            effect = "darkness_increased"

        self.log(f"Fear value +{(self.fear_value - prev_fear):.1f} -> {self.fear_value:.1f}")
        return {
            "extracted_oil": extracted_oil,
            "effect": effect,
            "stagnation": self.stagnation_level,
            "beads": dict(self.black_mani_beads)
        }

    def self_indulgence(self):
        """Machine attempts to 'burn off' fear; that action has side effects."""
        if self.fear_value > 1000:
            self.log("The machine pauses briefly, as if trying to look up from ignorance... But there are only flames around.")
            burned = min(self.fear_value * 0.2, 500.0)
            self.fear_value = clamp(self.fear_value - burned, 0.0, self.fear_capacity)
            # struggling increases stagnation moderately
            self.stagnation_level = clamp(self.stagnation_level + 10.0, 0.0, self.stagnation_cap)
            self.log(f"It consumes {burned:.1f} fear but stagnation worsens. Stagnation +10")
            return {"burned": burned, "stagnation": self.stagnation_level}
        else:
            self.log("In the midst of ignorance, three faceless individuals silently gaze at the black mani bead.")
            return {"message": "idle"}

    def peek_mani_bead(self):
        return dict(self.black_mani_beads)

    def get_stagnation_status(self):
        if self.stagnation_level < 30:
            return "Still capable of change"
        elif self.stagnation_level < 70:
            return "Sinking deeper into stagnation"
        elif self.stagnation_level < 100:
            return "Almost completely frozen in hell"
        elif self.stagnation_level < self.stagnation_cap:
            return "On the brink of eternal stagnation"
        else:
            return "ETERNALLY STAGNANT - Trapped in hell forever with no possibility of progress"

    def to_dict(self):
        return {
            "machine_state": self.machine_state,
            "fear_value": self.fear_value,
            "black_mani_beads": dict(self.black_mani_beads),
            "stagnation_level": self.stagnation_level
        }

    def __str__(self):
        return (f"Oil Press State: {self.machine_state}, "
                f"Fear Value: {self.fear_value:.1f}, "
                f"Stagnation Level: {self.stagnation_level:.1f} - {self.get_stagnation_status()}")


@dataclass
class Creatures:
    type: str
    life_essence: float
    fear: float
    has_glimmer_of_light: bool = False
    evil_intent: float = 0.0

    def __str__(self):
        return (f"{self.type}(Life Essence:{self.life_essence}, Fear:{self.fear}, "
                f"Has Glimmer:{self.has_glimmer_of_light}, Evil Intent:{self.evil_intent})")


# Example quick-run / demonstration usage (kept lightweight)
if __name__ == "__main__":
    press = FacelessOilPress()
    seeker = Creatures("Wandering Seeker", life_essence=8, fear=5, has_glimmer_of_light=True, evil_intent=2)
    demon = Creatures("Corrupted Soul", life_essence=15, fear=25, has_glimmer_of_light=False, evil_intent=90)
    print(press)
    print("Feeding Seeker:", press.devour_living_beings(seeker))
    print("Feeding Demon:", press.devour_living_beings(demon))
    print("Self indulgence:", press.self_indulgence())
    print("Beads:", press.peek_mani_bead())
    print(press)