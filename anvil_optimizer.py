enchant_data = {
    'protection': (4, 1, 1),
    'fire_protection': (4, 2, 1),
    'feather_falling': (4, 2, 1),
    'blast_protection': (4, 4, 2),
    'projectile_protection': (4, 2, 1),
    'thorns': (3, 8, 4),
    'respiration': (3, 4, 2),
    'depth_strider': (3, 4, 2),
    'aqua_affinity': (1, 4, 2),
    'sharpness': (5, 1, 1),
    'smite': (5, 2, 1),
    'bane_of_arthropods': (5, 2, 1),
    'knockback': (2, 2, 1),
    'fire_aspect': (2, 4, 2),
    'looting': (3, 4, 2),
    'efficiency': (5, 1, 1),
    'silk_touch': (1, 8, 4),
    'unbreaking': (3, 2, 1),
    'fortune': (3, 4, 2),
    'power': (5, 1, 1),
    'punch': (2, 4, 2),
    'flame': (1, 4, 2),
    'infinity': (1, 8, 4),
    'luck_of_the_sea': (3, 4, 2),
    'lure': (3, 4, 2),
    'frost_walker': (2, 4, 2),
    'mending': (1, 4, 2),
    'curse_of_binding': (1, 8, 4),
    'curse_of_vanishing': (1, 8, 4),
    'impaling': (5, 4, 2),
    'riptide': (3, 4, 2),
    'loyalty': (3, 1, 1),
    'channeling': (1, 8, 4),
    'multishot': (1, 4, 2),
    'piercing': (4, 1, 1),
    'quick_charge': (3, 2, 1),
    'soul_speed': (3, 8, 4),
    'swift_sneak': (3, 8, 4),
    'sweeping_edge': (3, 4, 2),
}


class Enchantable:
    def __init__(self, enchants=None, use_count=0, tool=False):
        self.use_count = use_count
        self.enchants = (enchants or {}).copy()
        self.cost = None
        self.is_tool = tool
    def get_penalty(self):
        return 2**self.use_count-1
    def __add__(target, sacrifice):
        result = Enchantable(
            enchants=target.enchants,
            use_count=max(target.use_count, sacrifice.use_count)+1,
            tool=target.is_tool or sacrifice.is_tool
        )
        result.cost = target.get_penalty()+sacrifice.get_penalty()
        for enchant, s_level in sacrifice.enchants.items():
            t_level = result.enchants.get(enchant, 0)
            level = t_level+1 if t_level == s_level else max(t_level, s_level)
            result.enchants[enchant] = level
            result.cost += level*enchant_data[enchant][2]
        return result
    def __repr__(self):
        return f'Enchantable(enchants={self.enchants}, use_count={self.use_count})'
    @staticmethod
    def solve(enchantables: list, max_cost: int=123456):
        if len(enchantables) <= 1: return 0
        if max_cost < 0: return max_cost
        min_cost = max_cost
        # print(enchantables, end='')
        for i, target in enumerate(enchantables):
            for j, sacrifice in enumerate(enchantables):
                if sacrifice.is_tool: continue
                if i == j: continue
                combined = target+sacrifice
                l, r = sorted((i, j))
                l_val, r_val = enchantables[l], enchantables[r]
                enchantables[l] = combined
                enchantables[r] = enchantables[-1]
                enchantables.pop()
                cost = Enchantable.solve(enchantables, min_cost-combined.cost)
                enchantables.append(r_val)
                enchantables[r], enchantables[-1] = enchantables[-1], enchantables[r]
                enchantables[l] = l_val
                cost += combined.cost
                min_cost = min(min_cost, cost)
        return min_cost


if __name__ == '__main__':
    import time

    # things = [
    #     Enchantable(tool=True),
    #     Enchantable({'sharpness': 5}),
    #     Enchantable({'efficiency': 5}),
    #     Enchantable({'fortune': 3}),
    #     Enchantable({'mending': 1}),
    #     Enchantable({'unbreaking': 3}),
    # ]

    things = [
        Enchantable(tool=True),
        Enchantable({'protection': 4}),
        Enchantable({'depth_strider': 3}),
        Enchantable({'feather_falling': 4}),
        Enchantable({'mending': 1}),
        Enchantable({'soul_speed': 3}),
        Enchantable({'unbreaking': 3}),
    ]

    # arr = list(things)
    # print(Enchantable.sum(arr))
    start = time.perf_counter()
    print(Enchantable.solve(things), 'levels')
    print(time.perf_counter()-start)