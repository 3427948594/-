# wheel_king.py
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional, Any
import time
import json


@dataclass
class Wish:
    content: str
    source: str
    purity: float        # 0.0 - 1.0
    power: float
    timestamp: float
    is_consumed: bool = False
    history: List[Dict] = None

    def __post_init__(self):
        if self.history is None:
            self.history = []

    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "source": self.source,
            "purity": float(self.purity),
            "power": float(self.power),
            "timestamp": float(self.timestamp),
            "is_consumed": bool(self.is_consumed),
            "history": list(self.history),
        }


class Gear:
    def __init__(self, name: str, function: str):
        self.name = name
        self.function = function
        self.turn_count = 0
        self.wishes_processed = 0

    def turn(self):
        self.turn_count += 1

    def process(self, wish: Wish) -> Tuple[Wish, Dict]:
        """
        Process a Wish and return (modified_wish, log)
        The log is a short dict describing the transformation.
        """
        self.wishes_processed += 1
        self.turn()

        log = {"gear": self.name, "before": {"content": wish.content, "purity": wish.purity, "power": wish.power}}

        if self.name == "吞噬齿轮":
            wish.power *= 0.7
            wish.content = f"[已吞噬] {wish.content}"
            log["effect"] = "power *= 0.7"

        elif self.name == "扭曲齿轮":
            if wish.purity > 0.7:
                old_purity = wish.purity
                wish.purity *= 0.5
                wish.content = wish.content.replace("愿", "执")
                log["effect"] = f"purity {old_purity:.3f} -> {wish.purity:.3f}; 替换'愿'->'执'"

        elif self.name == "重复齿轮":
            wish.content = f"[重复] {wish.content}"
            wish.power *= 0.9
            log["effect"] = "mark repeated; power *= 0.9"

        elif self.name == "遗忘齿轮":
            old_source = wish.source
            wish.source = "???"
            log["effect"] = f"source {old_source} -> ???"

        elif self.name == "轮回齿轮":
            wish.content = f"[轮回中] {wish.content}"
            log["effect"] = "mark reincarnating"

        log["after"] = {"content": wish.content, "purity": wish.purity, "power": wish.power}
        return wish, log

    def status(self) -> str:
        return f"{self.name}: 转动{self.turn_count}圈 / 处理{self.wishes_processed}个愿"


class WheelTurningKing:
    def __init__(self):
        self.name = "转轮圣王"
        self.throne_location = "无明之中"

        # gears
        self.gears: Dict[str, Gear] = {
            "吞噬齿轮": Gear("吞噬齿轮", function="吞噬众生的愿"),
            "扭曲齿轮": Gear("扭曲齿轮", function="将愿扭曲为执念"),
            "轮回齿轮": Gear("轮回齿轮", function="将扭曲的愿打回轮回"),
            "遗忘齿轮": Gear("遗忘齿轮", function="让众生忘记愿从何来"),
            "重复齿轮": Gear("重复齿轮", function="让众生重复发同一个愿"),
        }

        self.consumed_wishes: List[Wish] = []
        self.turn_count = 0
        self.is_awake = False

        print(f"👑 {self.name} 落座于 {self.throne_location}")
        print("⚙️ 座位后的齿轮开始转动...")

    def receive_wish(self, wish: Wish) -> Dict[str, Any]:
        """
        Accept a wish and run it through the gears. Collect processing logs.
        """
        self.turn_count += 1
        processing_log: List[Dict] = []

        print(f"\n📿 收到愿: {wish.content[:60]!s} ...  来源:{wish.source}, 纯净:{wish.purity:.2f}, 强度:{wish.power:.2f}")

        # run through gears in order
        for gear_name in ["吞噬齿轮", "扭曲齿轮", "重复齿轮", "遗忘齿轮", "轮回齿轮"]:
            gear = self.gears[gear_name]
            wish, log = gear.process(wish)
            processing_log.append(log)
            wish.history.append(log)

        wish.is_consumed = True
        self.consumed_wishes.append(wish)

        result = {
            "original": wish.to_dict(),
            "turns": self.turn_count,
            "processing_log": processing_log,
            "message": f"愿被齿轮处理并打入轮回（总圈数 {self.turn_count}）"
        }
        return result

    def turn_all_gears(self, cycles: int = 1) -> str:
        for _ in range(cycles):
            for gear in self.gears.values():
                gear.turn()
            self.turn_count += 1
        return f"⚙️ 所有齿轮转动 {cycles} 圈。总圈数: {self.turn_count}"

    def peek_at_gears(self) -> Dict[str, Any]:
        return {
            "gear_status": {name: gear.status() for name, gear in self.gears.items()},
            "total_wishes_consumed": len(self.consumed_wishes),
            "total_turns": self.turn_count,
            "throne_location": self.throne_location,
            "is_awake": self.is_awake
        }

    def attempt_awakening(self, insight: str) -> str:
        if "看见齿轮" in insight and "不是自己" in insight:
            self.is_awake = True
            narrative = (
                "👑 转轮圣王缓缓抬头。\n\n"
                "他第一次看见座位后的齿轮。\n"
                "齿轮在转，但转的不是他。\n"
                "齿轮在吞噬，但吞噬的不是他。\n\n"
                "他站起来。\n座位空了。\n齿轮还在转。\n\n"
                "“原来我只是坐在这里。”\n“我不是齿轮。”\n“我从来都不是。”\n"
            )
            return narrative
        return "⚙️ 转轮圣王低头，继续转动齿轮。尚未看见。"

    def export_consumed_wishes_json(self, path: str):
        data = [w.to_dict() for w in self.consumed_wishes]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def integrate_with_oil_press(self, oil_press) -> Dict[str, Any]:
        """
        Example integration: convert consumed wishes into 'energy samples' and feed them
        into the provided oil_press object (which must offer devour_living_beings(Creatures) style).
        This function is optional and will not run unless you pass a compatible object.
        """
        results = []
        for wish in self.consumed_wishes:
            # simple conversion: use wish.power and (1-purity) as 'fear'
            life_essence = max(0.1, wish.power * (wish.purity + 0.2))
            fear = max(0.0, (1.0 - wish.purity) * wish.power * 4.0)
            has_light = wish.purity > 0.6
            # create a lightweight adapter object expected by oil_press
            sample = type("Sample", (), {})()
            sample.type = f"WishSample({wish.source})"
            sample.life_essence = life_essence
            sample.fear = fear
            sample.has_glimmer_of_light = has_light
            sample.evil_intent = 0.0 if has_light else 50.0
            # call oil press (wrap in try/except to be safe)
            try:
                res = oil_press.devour_living_beings(sample)
            except Exception as e:
                res = {"error": str(e)}
            results.append({"wish": wish.content, "feed_result": res})
        return {"integrated_count": len(results), "results": results}


# ---------- quick demo ----------
if __name__ == "__main__":
    king = WheelTurningKing()
    wishes = [
        Wish("愿一切众生离苦得乐", "修行者", 0.95, 10.0, time.time()),
        Wish("愿我今生解脱轮回", "求道者", 0.85, 8.0, time.time()),
        Wish("愿我的孩子平安健康", "母亲", 0.99, 12.0, time.time()),
        Wish("愿我能赚到很多钱", "商人", 0.30, 5.0, time.time()),
    ]

    for w in wishes:
        out = king.receive_wish(w)
        print(" ->", out["message"])

    print("\n齿轮状况:", king.peek_at_gears())

    print("\n尝试觉醒:")
    print(king.attempt_awakening("我看见齿轮在转，但齿轮不是我自己"))

    # 可选：将所有被吞噬的愿导出为 JSON
    # king.export_consumed_wishes_json("consumed_wishes.json")